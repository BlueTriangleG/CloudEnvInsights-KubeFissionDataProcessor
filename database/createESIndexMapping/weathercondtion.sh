#!/bin/sh
curl -X PUT -k 'https://127.0.0.1:9200/mastodon-aus-social' \
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
        "id": { "type": "keyword" },
        "created_at": { "type": "date" },
        "lang": { "type": "keyword" },
        "sentiment": { "type": "float" },
        "tokens": { "type": "keyword" },
        "tags": { "type": "keyword" }
      }
    }
  }' \
  --user 'elastic:elastic' | jq '.'
