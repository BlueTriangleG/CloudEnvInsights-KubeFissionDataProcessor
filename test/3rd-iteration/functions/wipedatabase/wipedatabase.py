from flask import request, current_app
import requests, logging, json

def config(k):
    with open(f'/configs/default/parameters/{k}', 'r') as f:
       return f.read()

def main():
    r = requests.delete(f'{config("ES_URL")}/{config("ES_DATABASE")}',
            verify=False,
            auth=(config("ES_USERNAME"), config("ES_PASSWORD")))
    r = requests.put(f'{config("ES_URL")}/{config("ES_DATABASE")}',
            verify=False,
            auth=(config("ES_USERNAME"), config("ES_PASSWORD")),
            headers={'Content-type': 'application/json'},
            data=config("ES_SCHEMA"))

    return r.json(), r.status_code
