from elasticsearch import Elasticsearch, helpers
import json

# 初始化Elasticsearch客户端
es = Elasticsearch(
    hosts=['https://127.0.0.1:9200'],  
    basic_auth=('elastic', 'elastic'),  
    verify_certs=False  
)

# 读取JSON文件并将数据传输到Elasticsearch
def put_data_to_elasticsearch(index_name, json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)

    actions = [
        {
            "_index": index_name,
            "_id": doc['local_date_time_full'],
            "_source": doc
        }
        for doc in data
    ]

    helpers.bulk(es, actions)

if __name__ == "__main__":
    index_name = 'weathercondition'
    json_file = './data/pastData/pastWeatherCondition/weather.json'
    
    put_data_to_elasticsearch(index_name, json_file)
    print(f"Data from {json_file} has been successfully added to the {index_name} index in Elasticsearch.")
