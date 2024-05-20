import json
from elasticsearch import Elasticsearch, helpers
import pandas as pd

es = Elasticsearch(
    hosts=['https://127.0.0.1:9200/child-air-quality'],  
    basic_auth=('elastic', 'elastic'), 
    verify_certs=False 
)

def load_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def store_data_to_elasticsearch(data, index_name):
    print("starttransfer")
    actions = [
        {
            "_index": index_name,
            "_id": record['ogc_fid'], 
            "_source": record
        }
        for record in data
    ]
    helpers.bulk(es, actions)
    print(f'Successfully indexed {len(actions)} records')

def main():
    file_path = './data/childCareAirqualityData/child_care_with_air_quality.json'  
    data = load_json_file(file_path)
    store_data_to_elasticsearch(data, 'child-air-quality')  

if __name__ == "__main__":
    main()
