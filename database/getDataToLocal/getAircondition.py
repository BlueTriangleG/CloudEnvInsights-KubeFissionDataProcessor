from elasticsearch import Elasticsearch
import json
# 初始化Elasticsearch客户端
es = Elasticsearch(
    hosts=['https://127.0.0.1:9200'],  # 替换为您的Elasticsearch地址
    basic_auth=('elastic', 'elastic'),  # 替换为您的用户名和密码
    verify_certs=False  # 在生产环境中，建议启用证书验证
)

# 获取所有数据
def get_all_data(index_name):
    # 查询所有数据
    response = es.search(
        index=index_name,
        body={
            "query": {
                "match_all": {}
            }
        },
        size=10000  # 您可以调整大小以适应您的需求
    )
    return response['hits']['hits']

# 打印获取到的数据
if __name__ == "__main__":
    data = get_all_data('aircondition')
    # 把文件写入到文件
    with open('aircondition.json', 'w') as f:
        json.dump(data, f)
    for doc in data:
        print(doc['_source'])
