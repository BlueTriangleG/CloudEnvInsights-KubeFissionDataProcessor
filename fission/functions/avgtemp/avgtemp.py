import logging, json
from flask import current_app, request
from elasticsearch8 import Elasticsearch
from string import Template

days_expr= Template('''{
                           "range": {
                               "timestamp": {
                                   "gte": "${date}T00:00:00",
                                   "lte": "${date}T23:59:59"
                               }
                           }
                       }''')
station_expr= Template('''{
                      "bool": {
                          "must": [
                              {
                                  "match": {
                                      "stationid": "${station}"
                                  }
                              },
                              {
                                  "range": {
                                      "timestamp": {
                                          "gte": "${date}T00:00:00",
                                          "lte": "${date}T23:59:59"
                                      }
                                  }
                              }
                          ]
                      }
                  }''')

def main():
    try:
        date= request.headers['X-Fission-Params-Date']
    except KeyError:
         date= None

    try:
        station= request.headers['X-Fission-Params-Station']
    except KeyError:
         station= None

    client = Elasticsearch (
        'https://elasticsearch-master.elastic.svc.cluster.local:9200',
        verify_certs= False,
        basic_auth=('elastic', 'elastic')
    )

    if station is None:
      expr= days_expr.substitute(date=date)
    else:
      expr= station_expr.substitute(date=date, station=station)

    res= client.search(
      index='observations*',
      aggregations={
                       "avg_air_temp": {
                           "avg": {
                               "field": "air_temp"
                           }
                       }
                   },
      query=json.loads(expr)
    )

    return json.dumps(res['aggregations'])
