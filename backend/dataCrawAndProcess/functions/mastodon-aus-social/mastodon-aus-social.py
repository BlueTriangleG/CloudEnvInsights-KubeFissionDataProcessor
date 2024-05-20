from utils.mastodon import get_recent_timelines
import asyncio
from elasticsearch8 import Elasticsearch, helpers
import json
from flask import current_app, request

def store_data_to_elasticsearch(data):
    es = Elasticsearch(
    hosts=['https://elasticsearch-master.elastic.svc.cluster.local:9200'],
    basic_auth=('elastic', 'elastic'),
    verify_certs=False
    )
    actions = []
    for record in data:
        # input actions
        action = {
            "_index": "mastodon-aus-social",  
            "_id": record['id'],  
            "_source": record
        }
        actions.append(action)
    print(record)
    # input data
    helpers.bulk(es, actions)
    current_app.logger.info(f'Indexed finished')
    return 'ok'
    
def main():
    access_token = 'iq2gpUooJ10hAFXm19ifTGXitRWKs8KResFM-uMgEOY'
    instance_url = 'https://mastodon.social/'
    output_file = 'output.json'
    local = False

    loop = asyncio.get_event_loop()
    count = loop.run_until_complete(get_recent_timelines(access_token, instance_url, output_file, local))
    
    with open(output_file, 'r', encoding='utf-8') as file:
        data = [json.loads(line) for line in file]
    response = store_data_to_elasticsearch(data)
    print(count)
    return response

# if __name__ == '__main__':
#     print(main())