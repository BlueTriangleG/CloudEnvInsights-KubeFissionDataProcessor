from flask import request, current_app
import requests, logging, json

def config(k):
    with open(f'/configs/default/parameters/{k}', 'r') as f:
       return f.read()

def main():
    try:
        r = requests.post(f'{config("ES_URL")}/{config("ES_DATABASE")}/_search',
                verify=False,
                auth=(config('ES_USERNAME'), config('ES_PASSWORD')),
                headers={'Content-type': 'application/json'},
                data=json.dumps({'_source': False,
                    'query': {
                        'bool' : {
                          'must' : [
                            {
                                'term' : {
                                    'courses' : request.headers['X-Fission-Params-Courseid']
                                }
                            },
                            {
                                'term': {
                                    'type': 'student'
                                }
                            }
                          ]
                        }
                    },
                    'fields':[
                        {'field':'id'},
                        {'field':'timestamp'},
                        {'field':'name'}
                    ],
                    'sort': [
                        {
                          'name': {
                            'order': 'asc',
                            'missing': '_last',
                            'unmapped_type': 'keyword'
                         }
                       }
                    ]
                    })
                )
        return r.json(), r.status_code

    except Exception as e:
        current_app.logger.error(e)
        return {'message': f'Error {e}'}, 500



