import json
import requests

def send_data_to_cloud(index_name, json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    BASE_URL = "http://127.0.0.1:9090/database"
    url = f"{BASE_URL}/{index_name}"
    
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, json=data)
    
    return response

def main():
    index_name = 'aircondition'
    json_file = './data/pastData/pastAirCondition/aircondition.json'
    
    response = send_data_to_cloud(index_name, json_file)
    if response.status_code == 200:
        print(f"Data from {json_file} has been successfully added to the {index_name} index in Elasticsearch.")
    else:
        print(f"Failed to send data to Elasticsearch. Status code: {response.status_code}")
        print(f"Response: {response.text}")
        
if __name__ == "__main__":
    main()
