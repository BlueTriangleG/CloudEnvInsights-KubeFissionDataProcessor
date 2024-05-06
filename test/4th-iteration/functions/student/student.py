from flask import request, current_app
import requests, logging, json
from Commons import Commons
from ESStudent import ESStudent

def main():

    try:
        student = ESStudent(Commons(), request)

        if request.method == 'GET':
            r = requests.get(student.url(), verify=False, auth=Commons().auth())
            return r.json(), r.status_code

        elif request.method == 'PUT':
            r = requests.get(student.url(), verify=False, auth=Commons().auth())

            if r.status_code == 200:
                params={'if_seq_no': r.json()['_seq_no'], 'if_primary_term': r.json()['_primary_term']}
            else:
                params= {}

            r = requests.put(student.url(), verify=False, auth=Commons().auth(),
                    headers={'Content-type': 'application/json'},
                    data=json.dumps(student.add_fields(request.json)),
                    params=params)
            return r.json(), r.status_code

        elif request.method == 'DELETE':
            r = requests.get(student.url(), verify=False, auth=Commons().auth())

            if r.status_code != 200:
                return r.json(), r.status_code

            r = requests.delete(student.url(), verify=False, auth=Commons().auth(),
                params={'if_seq_no': r.json()['_seq_no'], 'if_primary_term': r.json()['_primary_term']})
            return r.json(), r.status_code
    except Exception as e:
        current_app.logger.error(e)
        return {'message': f'Error {e}'}, 500

    return {'message':'Method not allowed'}, 405
