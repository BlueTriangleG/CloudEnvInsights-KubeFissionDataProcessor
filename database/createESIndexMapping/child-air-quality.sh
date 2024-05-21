#!/bin/sh
curl -X PUT -k 'https://127.0.0.1:9200/child-air-quality' \
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
            "postcode": { "type": "float" },
            "legal_name": { "type": "text" },
            "suburb": { "type": "text" },
            "address": { "type": "text" },
            "ogc_fid": { "type": "integer" },
            "longitude": { "type": "float" },
            "latitude": { "type": "float" },
            "avg_air_quality": { "type": "float" }
        }
    }
}' \
  --user 'elastic:elastic' | jq '.'
