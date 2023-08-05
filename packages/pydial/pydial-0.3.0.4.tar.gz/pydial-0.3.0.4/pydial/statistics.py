import os
import json
import datetime
import geohash2
from elasticsearch import Elasticsearch


class DialStatisticsEngine(object):

    DEFAULT_NODE = {'host': 'localhost', 'port': 9200}
    MAX_ES_LIST_SIZE = 1024
    DEFAULT_TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'templates', 'statistics')

    def __init__(self, hosts=None, templates_directory=DEFAULT_TEMPLATE_DIR):
        if hosts is None:
            hosts = [self.DEFAULT_NODE]
        self.es_client = Elasticsearch(hosts)
        self.template_directory = templates_directory

    def get_statistics(self, pids=None, from_date=None, until_date=None, detail=False, localization=False):
        """ Get some usage statistics about a list of object from DIAL. This method will call DIAL ElasticSearch cluster
            to get some data, than aggregate these and anonymize these data and return the desired data

            :param pids: the list of pids to search. Must be an :class:`List` of basestring
            :param from_date: the lower limit interval where search about data. Must be a :class:`datetime.Datetime`
            :param until_date: the upper limit interval where search about data. Must be a :class:`datetime.Datetime`
            :param detail: ask for transaction detail (in this case, the information will not anonymized)
            :param localization: if you need information about localization transaction record (to play with map UI)
            :return a dictionary containing aggregate data and detailed data if requested
        """
        output = {
            'view': {
                'source': {'google': 0, 'uclouvain': 0, 'unamur': 0, 'other': 0},
                'total': 0,
            },
            'download': {
                'source': {'google': 0, 'uclouvain': 0, 'unamur': 0, 'other': 0},
                'total': 0,
            },
            'took': 0,
            'publication': {'counter': 0},
        }
        if pids is None:
            pids = []
        # because ElasticSearch 2.X can only play using list with 1024 elements, we need to split the :param:`pids` list
        # to several smaller list if size exceed 1024
        lol = lambda lst, size: [lst[i:i+size] for i in range(0, len(lst), size)]
        for pid_list in lol(pids, self.MAX_ES_LIST_SIZE):
            es_query = self._create_query(pid_list, from_date, until_date, detail, localization)
            r = self.es_client.search(index="logstash*", body=es_query)

            output['view']['source']['google'] += r['aggregations']['view']['buckets']['google']['doc_count']
            output['view']['source']['uclouvain'] += r['aggregations']['view']['buckets']['uclouvain']['doc_count']
            output['view']['source']['unamur'] += r['aggregations']['view']['buckets']['unamur']['doc_count']
            output['view']['source']['other'] += r['aggregations']['view']['buckets']['other']['doc_count']
            output['view']['total'] = sum([int(v) for v in output['view']['source'].values()])
            output['download']['source']['google'] += r['aggregations']['download']['buckets']['google']['doc_count']
            output['download']['source']['uclouvain'] += r['aggregations']['download']['buckets']['uclouvain']['doc_count']
            output['download']['source']['unamur'] += r['aggregations']['download']['buckets']['unamur']['doc_count']
            output['download']['source']['other'] += r['aggregations']['download']['buckets']['other']['doc_count']
            output['download']['total'] = sum([int(v) for v in output['download']['source'].values()])

            if detail:
                for name in [k for k in r['aggregations'].keys() if k not in ['view', 'download']]:
                    bucket_data = r['aggregations'][name]['buckets']
                    for action in ['view', 'download']:
                        if action not in bucket_data:
                            continue
                        output[action][name] = {}
                        for data in bucket_data[action]['dispatch']['buckets']:
                            key = data['key_as_string'] if 'key_as_string' in data else data['key']
                            output[action][name][key] = data['doc_count']
                        if 'sum_other_doc_count' in bucket_data[action]['dispatch'] \
                           and int(bucket_data[action]['dispatch']['sum_other_doc_count']) > 0:
                            output[action][name]['other'] = bucket_data[action]['dispatch']['sum_other_doc_count']
                if localization:
                    if 'localization' not in output:
                        output['localization'] = {}
                    for loc in r['aggregations']['localization']['buckets']:
                        point = geohash2.decode(loc['key'])
                        key = '[{lat},{lon}]'.format(lat=point[0], lon=point[1])
                        output['localization'][key] = localization['doc_count']
                if 'hits' not in output:
                    output['hits'] = []
                for hit in r['hits']['hits']:
                    output['hits'].append(hit['_source'])

            output['took'] += r['took']
            output['publication']['counter'] += len(pid_list)

    def _create_query(self, pids, from_date=None, until_date=None, detail=False, localization=False):
        # get basic query and set PID's parameter ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        with open(os.path.join(self.template_directory, 'basic_stat.tpl.json'), 'r') as fh:
            query = json.load(fh)
        quoted_pids = ['"{0}"'.format(p) for p in pids]
        query['query']['filtered']['query']['bool']['must'][0]['terms']['dial.pid.raw'] = quoted_pids
        # if time limit are specified, add the timestamp range filter ~~~~~~~~~~~~
        if from_date is not None or until_date is not None:
            with open(os.path.join(self.template_directory, 'timestamp_filter.tpl.json'), 'r') as fh:
                tstamp_filter = json.load(fh)
            if from_date is not None:
                from_epoch_millis = (from_date - datetime.datetime(1970, 1, 1)).total_seconds()*1000
                tstamp_filter['range']['@timestamp']['gte'] = from_epoch_millis
            if until_date is not None:
                until_epoch_millis = (until_date - datetime.datetime(1970, 1, 1)).total_seconds()*1000
                tstamp_filter['range']['@timestamp']['lte'] = until_epoch_millis
            query['query']['filtered']['filter']['bool']['must'].append(tstamp_filter)
        # add detail & localization aggregators if requested ~~~~~~~~~~~~~~~~~~~~~
        if detail:
            with open(os.path.join(self.template_directory, 'detail_aggs.tpl.json'), 'r') as fh:
                detail_aggs = json.load(fh)
            query['aggs'].update(detail_aggs)
            if localization:
                with open(os.path.join(self.template_directory, 'localization_aggs.tpl.json'), 'r') as fh:
                    localization_aggs = json.load(fh)
                query['aggs'].update(localization_aggs)
            query['size'] = 1000  # limit the detail response
        return query
