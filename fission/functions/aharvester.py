import logging, json, requests
from flask import current_app
from datetime import datetime, timedelta

def main():

    now = (datetime.utcnow() - timedelta(1)).isoformat()
    start = datetime.fromisoformat(now).replace(hour=0, minute=0, second=0).isoformat()
    end = datetime.fromisoformat(now).replace(hour=23, minute=59, second=59).isoformat()
    cql_filter= f"site_name='Mildura' and time_stamp>={start}Z and time_stamp<={end}Z"

    params = {
        'service': 'WFS',
        'version': '2.0.0',
        'request': 'GetFeature',
        'typeName': 'geonode:vic_observations_2023',
        'outputFormat': 'application/json',
        'cql_filter': cql_filter
    }

    data= requests.get("https://naqd.eresearch.unimelb.edu.au/geoserver/wfs", params=params).json()
    current_app.logger.info(f'Harvested one airquality observation')

    requests.post(url='http://router.fission/enqueue/airquality',
        headers={'Content-Type': 'application/json'},
        data=json.dumps(data)
    )
    return 'OK'
