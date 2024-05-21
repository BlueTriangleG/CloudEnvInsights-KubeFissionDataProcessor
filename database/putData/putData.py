import json

# read the json file and put data to Elasticsearch
def send_data_to_cloud(index_name, json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    print(data[0])

if __name__ == "__main__":
    index_name = 'aircondition'
    json_file = '../../data/pastData/pastAirCondition/aircondition.json'
    send_data_to_cloud(index_name, json_file)
    print(f"Data from {json_file} has been successfully added to the {index_name} index in Elasticsearch.")
