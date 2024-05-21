import logging
import json
import uuid
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
        es = Elasticsearch(
            hosts=['https://elasticsearch-master.elastic.svc.cluster.local:9200'],
            basic_auth=('elastic', 'elastic'),
            verify_certs=False
        )
        # Prepare the data for bulk insert
        actions = [
            {
                "_index": datatype,
                "_id": str(uuid.uuid4()),  # Generate a random UUID for each document
                "_source": doc
            }
            for doc in data
        ]
        # Insert the data to Elasticsearch
        helpers.bulk(es, actions)
        
        return 'finished', 200

    except Exception as e:
        logging.error(f"Error processing data for Elasticsearch: {e}")
        return json.dumps({"error": str(e)}), 500
