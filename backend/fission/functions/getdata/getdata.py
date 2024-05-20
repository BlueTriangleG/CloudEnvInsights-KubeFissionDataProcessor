import logging
import json
from flask import Flask, request
from elasticsearch8 import Elasticsearch

# Elasticsearch configuration
ES_HOST = 'https://elasticsearch-master.elastic.svc.cluster.local:9200'
ES_USER = 'elastic'
ES_PASSWORD = 'elastic'
# define query template
all_data_expr = {
    "match_all": {}
}

def main():
    try:
        try:
            datatype = request.headers['X-Fission-Params-Datatype']
        except KeyError:
            return json.dumps({"error": "Datatype header not found"}), 400

        client = Elasticsearch(
            ES_HOST,
            verify_certs=False,
            basic_auth=(ES_USER, ES_PASSWORD)
        )

        # use scroll to get all data
        scroll_timeout = "2m"
        page_size = 1000 

        res = client.search(
            index=datatype,
            body={
                "query": all_data_expr
            },
            scroll=scroll_timeout,
            size=page_size
        )

        scroll_id = res['_scroll_id']
        hits = res['hits']['hits']

        while len(res['hits']['hits']):
            res = client.scroll(
                scroll_id=scroll_id,
                scroll=scroll_timeout
            )
            scroll_id = res['_scroll_id']
            hits.extend(res['hits']['hits'])

        # clear scroll
        client.clear_scroll(scroll_id=scroll_id)

        # return the result
        return json.dumps(hits), 200

    except Exception as e:
        logging.error(f"Error fetching data from Elasticsearch: {e}")
        return json.dumps({"error": str(e)}), 500


