import logging
import json
from flask import request, Response
from elasticsearch8 import Elasticsearch
from string import Template


# Elasticsearch configuration
ES_HOST = 'https://elasticsearch-master.elastic.svc.cluster.local:9200'
ES_USER = 'elastic'
ES_PASSWORD = 'elastic'

# Define query template
all_data_expr = Template('''{
    "match_all": {}
}''')



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

        client = Elasticsearch(
            ES_HOST,
            verify_certs=False,
            basic_auth=(ES_USER, ES_PASSWORD)
        )

        query = all_data_expr.substitute()
        # execute query
        query_body = {
            "query": json.loads(query)
        }
        print(query_body)
        return Response(generate_chunks(client, datatype, query_body), content_type='application/json')

    except Exception as e:
        logging.error(f"Error fetching data from Elasticsearch: {e}")
        return json.dumps({"error": str(e)}), 500
