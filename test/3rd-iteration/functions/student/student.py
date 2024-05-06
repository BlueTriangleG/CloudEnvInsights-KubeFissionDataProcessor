from flask import request, current_app
import requests, logging, json
from datetime import datetime

def config(k):
    with open(f'/configs/default/parameters/{k}', 'r') as f:
       return f.read()

def docurl():
    return f'{config("ES_URL")}/{config("ES_DATABASE")}/_doc/student_{request.headers["X-Fission-Params-Studentid"]}'

def addfields(data):
    data['timestamp'] = datetime.now().isoformat()
    data['id'] = request.headers['X-Fission-Params-Studentid']
    data['type'] = 'student'
    return data

def main():
    try:
        if request.method == 'GET':
            r = requests.get(docurl(), verify=False, auth=(config("ES_USERNAME"), config("ES_PASSWORD")))
            return r.json(), r.status_code

        elif request.method == 'PUT':
            r = requests.get(docurl(), verify=False, auth=(config("ES_USERNAME"), config("ES_PASSWORD")))

            if r.status_code == 200:
                params={'if_seq_no': r.json()['_seq_no'], 'if_primary_term': r.json()['_primary_term']}
            else:
                params= {}

            r = requests.put(docurl(), verify=False, auth=(config("ES_USERNAME"), config("ES_PASSWORD")),
                    headers={'Content-type': 'application/json'},
                    data=json.dumps(addfields(request.json)),
                    params=params)
            return r.json(), r.status_code

        elif request.method == 'DELETE':
            r = requests.get(docurl(), verify=False, auth=(config("ES_USERNAME"), config("ES_PASSWORD")))

            if r.status_code != 200:
                return r.json(), r.status_code

            r = requests.delete(docurl(), verify=False, auth=(config("ES_USERNAME"), config("ES_PASSWORD")),
                    params={'if_seq_no': r.json()['_seq_no'], 'if_primary_term': r.json()['_primary_term']})
            return r.json(), r.status_code
    except Exception as e:
        current_app.logger.error(e)
        return {'message': f'Error {e}'}, 500

    return {'message':'Method not allowed'}, 405
