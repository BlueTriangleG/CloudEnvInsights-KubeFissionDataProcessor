from elasticsearch import Elasticsearch
import json

es = Elasticsearch(
    hosts=['https://127.0.0.1:9200'], 
    basic_auth=('elastic', 'elastic'), 
    verify_certs=False  )

def get_all_data(index_name):
    response = es.search(
        index=index_name,
        body={
            "query": {
                "match_all": {}
            }
        },
        size=10000  
    )
    return response['hits']['hits']

if __name__ == "__main__":
    data = get_all_data('weathercondition')
    with open('./data/weather.json', 'w') as f:
        json.dump(data, f)
    for doc in data:
        print(doc['_source'])
