from elasticsearch import Elasticsearch
import json

def create_air_quality_index(context):
    req = json.loads(context.request.body)
    es_url = req.get('url')
    es = Elasticsearch([es_url])

    index_name = "airQuality"
    settings = {
        "settings": {
            "number_of_shards": 3,
            "number_of_replicas": 1
        },
        "mappings": {
            "properties": {
                "BPM2_5": { "type": "float" },
                "datetime_local": { "type": "date", "format": "yyyy-MM-dd-HH" },
                "location_name": { "type": "keyword" }
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
    result = create_air_quality_index(context)

if __name__ == "__main__":
    main()

