from elasticsearch import Elasticsearch
import json
# initialize the Elasticsearch client
es = Elasticsearch(
    hosts=['https://127.0.0.1:9200'],  
    basic_auth=('elastic', 'elastic'),  
    verify_certs=False  
)

# get all data
def get_all_data(index_name):
    # query all data
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
    data = get_all_data('aircondition')
    # write the file
    with open('./data/aircondition.json', 'w') as f:
        json.dump(data, f)
    for doc in data:
        print(doc['_source'])
