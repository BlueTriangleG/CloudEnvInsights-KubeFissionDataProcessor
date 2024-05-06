from flask import request, current_app
import requests, logging, json
from Commons import Commons

def main():
    try:
        r = requests.post(Commons.search_url(),
                verify=False,
                auth=Commons().auth(),
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



