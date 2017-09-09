from elasticsearch import Elasticsearch

es = Elasticsearch("http://127.0.0.1:9000")

query = '{"query":{"bool":{"must":[{"wildcard":{"peerType.keyword":"*cowrie*"}},{"wildcard":{"login.keyword":"*Success*"}}],"must_not":[],"should":[]}},"from":0,"size":9000,"sort":[],"aggs":{}}'
res = es.search(index="ews2017.1", doc_type="Alert", body=query)

for hit in res['hits']['hits']:

    requestString = "%(originalRequestString)s " % hit["_source"]
    print("Found SSH code:" + requestString)