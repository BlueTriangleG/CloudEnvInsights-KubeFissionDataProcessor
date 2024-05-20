import json
from elasticsearch import Elasticsearch, helpers
import uuid

es = Elasticsearch(
    hosts=['https://127.0.0.1:9200'],  
    basic_auth=('elastic', 'elastic'),  
    verify_certs=False  
)

def load_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = [json.loads(line) for line in file]
    return data

def store_data_to_elasticsearch(data, index_name):
    actions = []
    for record in data:
        # generate a random UUID as the document ID
        doc_id = str(uuid.uuid4())
        
        action = {
            "_index": index_name,
            "_id": doc_id,  # Use the randomly generated UUID as the Elasticsearch document ID
            "_source": record
        }
        actions.append(action)
    
    # Bulk insert data
    helpers.bulk(es, actions)
    print(f'Successfully indexed {len(actions)} records')

def main():
    file_path = './data/realestateVSaffordabilityData/final_data.json'  
    data = load_json_file(file_path)
    store_data_to_elasticsearch(data, 'realestate-affordability')  

if __name__ == "__main__":
    main()
