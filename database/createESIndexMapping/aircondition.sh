#!/bin/sh
curl -X PUT -k 'https://127.0.0.1:9200/aircondition' \
  --header 'Content-Type: application/json' \
  --data '{
    "settings": {
        "index": {
            "number_of_shards": 3,
            "number_of_replicas": 1
        }
    },
    "mappings": {
        "properties": {
            "BMP2_5": {
              "type": "float"
            },
            "datetime_local": {
              "type": "date",
              "format": "yyyy-MM-dd-HH"
            },
            "location_name": {
              "type": "keyword"
            }
      }
    }
  }' \
  --user 'elastic:elastic' | jq '.'
