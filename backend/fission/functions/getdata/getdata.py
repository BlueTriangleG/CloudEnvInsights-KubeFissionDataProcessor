import logging
import json
from flask import Flask, request
from elasticsearch8 import Elasticsearch

# Elasticsearch配置
ES_HOST = 'https://elasticsearch-master.elastic.svc.cluster.local:9200'
ES_USER = 'elastic'
ES_PASSWORD = 'elastic'

# 定义查询模板
all_data_expr = {
    "match_all": {}
}

def main():
    try:
        try:
            datatype = request.headers['X-Fission-Params-Datatype']
        except KeyError:
            return json.dumps({"error": "Datatype header not found"}), 400

        # 初始化Elasticsearch客户端
        client = Elasticsearch(
            ES_HOST,
            verify_certs=False,
            basic_auth=(ES_USER, ES_PASSWORD)
        )

        # 执行查询
        res = client.search(
            index=datatype,
            query=all_data_expr
        )

        # 提取响应数据
        response_data = res.body

        # 返回查询结果
        return json.dumps(response_data), 200

    except Exception as e:
        logging.error(f"Error fetching data from Elasticsearch: {e}")
        return json.dumps({"error": str(e)}), 500
