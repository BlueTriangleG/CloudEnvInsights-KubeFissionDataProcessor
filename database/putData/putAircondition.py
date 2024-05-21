from elasticsearch import Elasticsearch, helpers
import json
import uuid

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
    
    actions = []
    for doc in data:
        data = doc["_source"]
        bpm2_5 = data["BMP2_5"]
        datetime_local = data["datetime_local"]
        location_name = data["location_name"]
        
        actions.append({
            "_index": index_name,
            "_id": str(uuid.uuid4()),
            "_source": {
                "BPM2_5": bpm2_5,
                "datetime_local": datetime_local,
                "location_name": location_name
            }
        })
        
        
    
    print(actions[1])

    helpers.bulk(es, actions)

if __name__ == "__main__":
    index_name = 'aircondition'
    json_file = './data/pastData/pastAirCondition/aircondition.json'
    
    put_data_to_elasticsearch(index_name, json_file)
    print(f"Data from {json_file} has been successfully added to the {index_name} index in Elasticsearch.")
