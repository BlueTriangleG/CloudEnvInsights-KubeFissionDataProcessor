from flask import request, current_app
import requests, logging, json
from datetime import datetime

class ESDocument:
    def __init__(self, commons, req, type):
        self.commons = commons
        self.req = req
        self.type = type

    def url(self):
        return f'{self.commons.config("ES_URL")}/{self.commons.config("ES_DATABASE")}/_doc/{self.type}_{self.req.headers[f"X-Fission-Params-{self.type.capitalize()}id"]}'

    def add_fields(self, data):
        data['timestamp'] = datetime.now().isoformat()
        data['id'] = self.req.headers[f'X-Fission-Params-{self.type.capitalize()}id']
        data['type'] = self.type
        return data

    def get(self):
        r = requests.get(self.doc_url(), verify=False, auth=self.commons.auth())
        return r.json(), r.status_code

    def put(self):
        r = requests.get(self.doc_url(), verify=False, auth=self.commons.auth())

        if r.status_code == 200:
            params={'if_seq_no': r.json()['_seq_no'], 'if_primary_term': r.json()['_primary_term']}
        else:
            params= {}

        r = requests.put(self.doc_url(), verify=False, auth=self.commons.auth(),
                headers={'Content-type': 'application/json'},
                data=json.dumps(self.add_fields(request.json)),
                params=params)
        return r.json(), r.status_code

    def delete(self):
        r = requests.get(self.doc_url(), verify=False, auth=self.commons.auth())

        if r.status_code != 200:
            return r.json(), r.status_code

        r = requests.delete(doc_url(), verify=False, auth=self.commons.auth(),
                params={'if_seq_no': r.json()['_seq_no'], 'if_primary_term': r.json()['_primary_term']})
        return r.json(), r.status_code

    def all(self):
        return json.dumps({'_source': False,
                    'query': {
                        'term': {
                            'type': {
                                'value': f'{self.type}'
                            }
                        }
                    },
                    'fields':[
                        {'field':'id'},
                        {'field':'timestamp'},
                        {'field':'name'},
                        {'field':'courses'}
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
