import logging
import json
import requests
from flask import current_app, request
from elasticsearch8 import Elasticsearch

def main():
    client = Elasticsearch(
        'https://elasticsearch-master.elastic.svc.cluster.local:9200',
        verify_certs=False,
        basic_auth=('elastic', 'elastic')
    )

    observations = request.get_json(force=True)
    current_app.logger.info(f'Observations to add: {observations}')

    for obs in observations:
        res = client.index(
            index='observations',
            id=f'{obs["stationid"]}-{obs["timestamp"]}',
            body=obs
        )
        current_app.logger.info(f'Indexed observation {obs["stationid"]}-{obs["timestamp"]}')

    return 'ok'