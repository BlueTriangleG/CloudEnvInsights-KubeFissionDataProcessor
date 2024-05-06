from flask import request, current_app
import requests, logging, json
from Commons import Commons

def main():
    r = requests.delete(f'{Commons.config("ES_URL")}/{Commons.config("ES_DATABASE")}',
            verify=False,
            auth=Commons.auth())
    r = requests.put(f'{Commons.config("ES_URL")}/{Commons.config("ES_DATABASE")}',
            verify=False,
            auth=Commons.auth(),
            headers={'Content-type': 'application/json'},
            data=Commons.config("ES_SCHEMA"))

    return r.json(), r.status_code
