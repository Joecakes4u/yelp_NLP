from elasticsearch import Elasticsearch
def parse(file=None):
    try:
        with open(file, 'r') as myfile:
            data=myfile.read().split('\n')
        es = Elasticsearch(['localhost:9200'], http_auth=('elastic','changeme'))
        i = 1
        for d in data:
            res = es.index(index="yelp", doc_type='review', id=i, body=d)
            i += 1
            print(str(i)+": "+str(res['created']))
    except Exception as e:
        print str(e)

if __name__ == "__main__":
    # insert file path
    file = ""
    parse(file)
