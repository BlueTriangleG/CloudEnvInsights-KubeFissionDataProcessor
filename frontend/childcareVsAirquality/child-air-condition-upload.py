import json
from elasticsearch import Elasticsearch, helpers
import pandas as pd

# 初始化Elasticsearch客户端
es = Elasticsearch(
    hosts=['https://127.0.0.1:9200/child-air-quality'],  # 替换为您的Elasticsearch地址
    basic_auth=('elastic', 'elastic'),  # 替换为您的用户名和密码
    verify_certs=False  # 在生产环境中，建议启用证书验证
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
            "_id": record['ogc_fid'],  # 使用文档中的ogc_fid字段作为Elasticsearch文档ID
            "_source": record
        }
        for record in data
    ]
    helpers.bulk(es, actions)
    print(f'Successfully indexed {len(actions)} records')

def main():
    file_path = './fission/childcareVsAirquality/child_care_with_air_quality.json'  # 替换为您的JSON文件路径
    data = load_json_file(file_path)
    store_data_to_elasticsearch(data, 'child-air-quality')  # 替换为您的索引名称

if __name__ == "__main__":
    main()
