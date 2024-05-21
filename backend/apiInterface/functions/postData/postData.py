import logging
import json
from flask import request, Response
from elasticsearch8 import Elasticsearch, helpers

# Elasticsearch configuration
ES_HOST = 'https://elasticsearch-master.elastic.svc.cluster.local:9200'
ES_USER = 'elastic'
ES_PASSWORD = 'elastic'

def main():
    try:
        try:
            datatype = request.headers['X-Fission-Params-Datatype']
        except KeyError:
            return json.dumps({"error": "Datatype header not found"}), 400
        # Check if the request body is empty
        data = request.json
        if not data:
            return json.dumps({"error": "Request body is empty or not a valid JSON"}), 400
        # Initialize the Elasticsearch client
        client = Elasticsearch(
            ES_HOST,
            verify_certs=False,
            basic_auth=(ES_USER, ES_PASSWORD)
        )
        # Prepare the data for bulk insert
        actions = [
            {
                "_index": datatype,
                "_id": doc['datetime_local'],
                "_source": doc
            }
            for doc in data
        ]
        # Insert the data to Elasticsearch
        helpers.bulk(client, actions)
        
        return 'finished', 200

    except Exception as e:
        logging.error(f"Error processing data for Elasticsearch: {e}")
        return json.dumps({"error": str(e)}), 500
