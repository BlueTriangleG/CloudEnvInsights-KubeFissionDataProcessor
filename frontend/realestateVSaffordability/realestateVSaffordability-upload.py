import json
from elasticsearch import Elasticsearch, helpers
import uuid

# 初始化Elasticsearch客户端
es = Elasticsearch(
    hosts=['https://127.0.0.1:9200'],  # 替换为您的Elasticsearch地址
    basic_auth=('elastic', 'elastic'),  # 替换为您的用户名和密码
    verify_certs=False  # 在生产环境中，建议启用证书验证
)

def load_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = [json.loads(line) for line in file]
    return data

def store_data_to_elasticsearch(data, index_name):
    actions = []
    for record in data:
        # 生成一个随机的UUID作为文档ID
        doc_id = str(uuid.uuid4())
        
        # 构建每个文档的索引请求
        action = {
            "_index": index_name,
            "_id": doc_id,  # 使用随机生成的UUID作为Elasticsearch文档ID
            "_source": record
        }
        actions.append(action)
    
    # 批量插入数据
    helpers.bulk(es, actions)
    print(f'Successfully indexed {len(actions)} records')

def main():
    file_path = './fission/realestateVSaffordability/path/final_data.json'  # 替换为您的JSON文件路径
    data = load_json_file(file_path)
    store_data_to_elasticsearch(data, 'realestate-affordability')  # 替换为您的索引名称

if __name__ == "__main__":
    main()
