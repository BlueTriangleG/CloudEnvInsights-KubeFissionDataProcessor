import logging
import json
from flask import Flask, request, Response
from elasticsearch8 import Elasticsearch
from string import Template
from datetime import datetime, timezone


# Elasticsearch configuration
ES_HOST = 'https://elasticsearch-master.elastic.svc.cluster.local:9200'
ES_USER = 'elastic'
ES_PASSWORD = 'elastic'


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
    "range": {
        "created_at": {
            "gte": "${start_date}",
            "lte": "${end_date}"
        }
    }
}''')

def convert_date(date_string):
    date_obj = datetime.strptime(date_string, "%Y-%m-%d-%H")
    iso_format_str = date_obj.replace(tzinfo=timezone.utc).isoformat()
    logging.info(f"Converted date: {iso_format_str}")
    return str(iso_format_str)

def generate_chunks(client, datatype, query, scroll_timeout="5m", page_size=1000):
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
        logging.error(f"Error fetching data from Elasticsearch: {e}")
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

        if datatype == 'aircondition':
            query = time_period_expr_aircondition.substitute(start_date=start_date, end_date=end_date)
        elif datatype == 'weathercondition':
            query = time_period_expr_weathercondition.substitute(start_date=start_date, end_date=end_date)
        elif datatype == 'mastodon-aus-social':
            start_date = convert_date(start_date)
            end_date = convert_date(end_date)
            query = time_period_expr_mastodon_aus_social.substitute(start_date=start_date, end_date=end_date)
        else:
            return json.dumps({"error": "Invalid datatype"}), 400

        # execute query
        query_body = {
            "query": json.loads(query)
        }
        print(query_body)
        return Response(generate_chunks(client, datatype, query_body), content_type='application/json')

    except Exception as e:
        logging.error(f"Error fetching data from Elasticsearch: {e}")
        return json.dumps({"error": str(e)}), 500
