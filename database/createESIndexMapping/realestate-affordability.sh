curl -X PUT -k 'https://127.0.0.1:9200/realestate-affordability' \
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
            "building_address": { "type": "text" },
            "clue_small_area": { "type": "text" },
            "dwelling_type": { "type": "text" },
            "longitude": { "type": "float" },
            "latitude": { "type": "float" },
            "geography_name": { "type": "text" },
            "rai_national_total_2014_q2": { "type": "float" },
            "rai_national_total_2014_q3": { "type": "float" },
            "rai_national_total_2014_q4": { "type": "float" },
            "rai_national_total_2021_q1": { "type": "float" },
            "rai_national_total_2014_q1": { "type": "float" },
            "state": { "type": "keyword" },
            "rai_national_total_2020_q1": { "type": "float" },
            "rai_national_total_2020_q2": { "type": "float" },
            "rai_national_total_2020_q3": { "type": "float" },
            "rai_national_total_2011_q2": { "type": "float" },
            "rai_national_total_2020_q4": { "type": "float" },
            "rai_national_total_2011_q1": { "type": "float" },
            "city": { "type": "keyword" },
            "unique_id": { "type": "integer" },
            "rai_national_total_2013_q3": { "type": "float" },
            "rai_national_total_2013_q4": { "type": "float" },
            "rai_national_total_2013_q1": { "type": "float" },
            "rai_national_total_2012_q4": { "type": "float" },
            "rai_national_total_2013_q2": { "type": "float" },
            "rai_national_total_2015_q3": { "type": "float" },
            "rai_national_total_2015_q4": { "type": "float" },
            "rai_national_total_2015_q1": { "type": "float" },
            "rai_national_total_2015_q2": { "type": "float" },
            "rai_national_total_2016_q1": { "type": "float" },
            "rai_national_total_2016_q2": { "type": "float" },
            "rai_national_total_2016_q3": { "type": "float" },
            "rai_national_total_2016_q4": { "type": "float" },
            "rai_national_total_2012_q1": { "type": "float" },
            "rai_national_total_2012_q3": { "type": "float" },
            "rai_national_total_2012_q2": { "type": "float" },
            "rai_national_total_2017_q3": { "type": "float" },
            "rai_national_total_2017_q4": { "type": "float" },
            "rai_national_total_2019_q1": { "type": "float" },
            "rai_national_total_2017_q1": { "type": "float" },
            "rai_national_total_2019_q2": { "type": "float" },
            "rai_national_total_2017_q2": { "type": "float" },
            "rai_national_total_2011_q4": { "type": "float" },
            "rai_national_total_2018_q4": { "type": "float" },
            "rai_national_total_2018_q3": { "type": "float" },
            "rai_national_total_2018_q2": { "type": "float" },
            "rai_national_total_2018_q1": { "type": "float" },
            "rai_national_total_2021_q2": { "type": "float" },
            "rai_national_total_2019_q3": { "type": "float" },
            "rai_national_total_2019_q4": { "type": "float" }
        }
    }
}' \
  --user 'elastic:elastic' | jq '.'
