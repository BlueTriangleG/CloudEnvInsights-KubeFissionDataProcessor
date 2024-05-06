from flask import request, current_app
import requests, logging, json
from Commons import Commons
from ESStudent import ESStudent

def main():
    try:
        r = requests.post(Commons().search_url(),
                verify=False,
                auth=Commons().auth(),
                headers={'Content-type': 'application/json'},
                data= ESStudent(Commons(), request).all()
                )
        return r.json(), r.status_code

    except Exception as e:
        current_app.logger.error(e)
        return {'message': f'Error {e}'}, 500

    return {'message':'Method not allowed'}, 405

