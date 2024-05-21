#!/bin/sh
curl -X PUT -k 'https://127.0.0.1:9200/weathercondition' \
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
          "air_temp": {
            "type": "float"
          },
          "apparent_t": {
            "type": "float"
          },
          "delta_t": {
            "type": "float"
          },
          "dewpt": {
            "type": "float"
          },
          "gust_kmh": {
            "type": "float"
          },
          "gust_kt": {
            "type": "float"
          },
          "lat": {
            "type": "float"
          },
          "local_date_time_full": {
            "type": "date",
            "format": "yyyy-MM-dd-HH"
          },
          "lon": {
            "type": "float"
          },
          "name": {
            "type": "keyword"
          },
          "press": {
            "type": "float"
          },
          "press_msl": {
            "type": "float"
          },
          "press_qnh": {
            "type": "float"
          },
          "rel_hum": {
            "type": "integer"
          },
          "wind_dir": {
            "type": "keyword"
          },
          "wind_spd_kmh": {
            "type": "float"
          },
          "wind_spd_kt": {
            "type": "float"
          }
        }
    }
  }' \
  --user 'elastic:elastic' | jq '.'
