import logging
import json
from flask import Flask, request, Response
from elasticsearch import Elasticsearch
from string import Template
from datetime import datetime, timezone


# Elasticsearch configuration
ES_HOST = 'https://elasticsearch-master.elastic.svc.cluster.local:9200'
ES_USER = 'elastic'
ES_PASSWORD = 'elastic'

# Define query template
all_data_expr = Template('''{
    "match_all": {}
}''')

time_period_expr_aircondition = Template('''{
    "range": {
        "datetime_local": {
            "gte": "${start_date}",
            "lte": "${end_date}",
            "format": "yyyy-MM-dd-HH"
        }
    }
}''')

time_period_expr_weathercondition = Template('''{
    "range": {
        "local_date_time_full": {
            "gte": "${start_date}",
            "lte": "${end_date}",
            "format": "yyyy-MM-dd-HH"
        }
    }
}''')

time_period_expr_mastodon_aus_social = Template('''{
    "match_all": {}
}''')

def convert_date(date_string):
    # 解析日期字符串为datetime对象
    date_obj = datetime.strptime(date_string, "%Y-%m-%d-%H")
    
    # 将datetime对象转换为ISO 8601格式的字符串，并添加时区信息（假设为UTC）
    iso_format_str = date_obj.replace(tzinfo=timezone.utc).isoformat()
    
    # 记录转换后的日期
    logging.info(f"Converted date: {iso_format_str}")
    
    # 确保返回值为字符串
    return str(iso_format_str)

def generate_chunks(client, datatype, query, scroll_timeout="2m", page_size=1000):
    try:
        res = client.search(
            index=datatype,
            body=query,
            scroll=scroll_timeout,
            size=page_size
        )
        scroll_id = res['_scroll_id']
        hits = res['hits']['hits']
        yield json.dumps(hits) + '\n'

        while len(res['hits']['hits']):
            res = client.scroll(
                scroll_id=scroll_id,
                scroll=scroll_timeout
            )
            scroll_id = res['_scroll_id']
            hits = res['hits']['hits']
            yield json.dumps(hits) + '\n'

        # clear scroll
        client.clear_scroll(scroll_id=scroll_id)

    except Exception as e:
        logging.error(f"Second Error fetching data from Elasticsearch: {e}")
        yield json.dumps({"error": str(e)}) + '\n'
    
def main():
    try:
        try:
            datatype = request.headers['X-Fission-Params-Datatype']
        except KeyError:
            return json.dumps({"error": "Datatype header not found"}), 400
        
        try:
            start_date = request.headers['X-Fission-Params-Startdate']
            end_date = request.headers['X-Fission-Params-Enddate']
        except KeyError:
            start_date = None
            end_date = None

        client = Elasticsearch(
            ES_HOST,
            verify_certs=False,
            basic_auth=(ES_USER, ES_PASSWORD)
        )

        if end_date is None:
            query = all_data_expr.substitute()
        else:
            if datatype == 'aircondition':
                query = time_period_expr_aircondition.substitute(start_date=start_date, end_date=end_date)
            elif datatype == 'weathercondition':
                query = time_period_expr_weathercondition.substitute(start_date=start_date, end_date=end_date)
            elif datatype == 'mastodon-aus-social':
                start_date = convert_date(start_date)
                end_date = convert_date(end_date)
                query = all_data_expr.substitute()

        # execute query
        query_body = {
            "query": json.loads(query)
        }
        print(query_body)
        return Response(generate_chunks(client, datatype, query_body), content_type='application/json')

    except Exception as e:
        logging.error(f"First Error fetching data from Elasticsearch: {e}")
        return json.dumps({"error": str(e)}), 500
