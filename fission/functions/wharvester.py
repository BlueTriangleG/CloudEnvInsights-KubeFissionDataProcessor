import logging, json, requests, socket
from flask import current_app

def main():

    data= requests.get('http://reg.bom.gov.au/fwo/IDV60901/IDV60901.95936.json').json()
    current_app.logger.info(f'Harvested one weather observation')

    requests.post(url='http://router.fission/enqueue/weather',
        headers={'Content-Type': 'application/json'},
        data=json.dumps(data)
    )
    return 'OK'
