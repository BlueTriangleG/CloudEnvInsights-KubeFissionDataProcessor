from elasticsearch import Elasticsearch
import json

def create_weather_index(context):
    req = json.loads(context.request.body)
    es_url = req.get('url')
    es = Elasticsearch([es_url])

    index_name = "weather"
    settings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 1
        },
        "mappings": {
            "properties": {
                "name": { "type": "keyword" },
                "local_date_time_full": { "type": "date", "format": "yyyy-MM-dd-HH" },
                "lat": { "type": "float" },
                "lon": { "type": "float" },
                "apparent_t": { "type": "float" },
                "delta_t": { "type": "float" },
                "gust_kmh": { "type": "float" },
                "gust_kt": { "type": "float" },
                "air_temp": { "type": "float" },
                "dewpt": { "type": "float" },
                "press": { "type": "float" },
                "press_qnh": { "type": "float" },
                "press_msl": { "type": "float" },
                "rel_hum": { "type": "integer" },
                "wind_dir": { "type": "keyword" },
                "wind_spd_kmh": { "type": "float" },
                "wind_spd_kt": { "type": "float" }
            }
        }
    }

    # create index
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name, body=settings)
        print(f"Index {index_name} created with specified mappings.")
    else:
        print(f"Index {index_name} already exists.")


def main(context):
    result = create_weather_index(context)

if __name__ == "__main__":
    main()
