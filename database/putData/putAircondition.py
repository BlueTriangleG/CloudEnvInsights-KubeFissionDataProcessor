from elasticsearch import Elasticsearch, helpers
import json

# initialize the Elasticsearch client
es = Elasticsearch(
    hosts=['https://127.0.0.1:9200'],  
    basic_auth=('elastic', 'elastic'),  
    verify_certs=False  
)

# read the json file and put data to Elasticsearch
def put_data_to_elasticsearch(index_name, json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)

    actions = [
        {
            "_index": index_name,
            "_id": doc['datetime_local'],
            "_source": doc
        }
        for doc in data
    ]
    print(actions[1])

    helpers.bulk(es, actions)

if __name__ == "__main__":
    index_name = 'aircondition'
    json_file = './data/pastData/pastAirCondition/air.json'
    
    put_data_to_elasticsearch(index_name, json_file)
    print(f"Data from {json_file} has been successfully added to the {index_name} index in Elasticsearch.")
