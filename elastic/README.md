### FILE STRUCTURE
# ./mapping
for all mappings and initialisations
# ./crud
for create delete read and update basic methods
# ./querying
for advanced query operations including merging ability
# ./utils
for flask router and helper functions
# ./example
teacher's test example for localhost elastic search

### CREATE INDEX (INITIALISATION)
# main() have been implemented so that you can directly fission it by:
fission function update --name create_indexes --env python --code <genshin!>_mapping.py --method POST
# using by post and passing context like this: (change it to real API)
{"url": "http://local-elasticsearch:9200"}
# whole POST command example here!
curl -X POST http://$FISSION_ROUTER/create-<what>-index -H "Content-Type: application/json" -d '{"url": "http://local-elasticsearch:9200"}'

### USE CRUD
# Create example
curl -X POST http://localhost:5000/create -H "Content-Type: application/json" -d '{
  "url": "http://localhost:9200",
  "data": {
    "index": "airQuality",
    "BPM2_5": 12.34,
    "datetime_local": "2023-01-01-12",
    "location_name": "San Francisco"
  }
}'
# Delete example
curl -X POST http://localhost:5000/delete -H "Content-Type: application/json" -d '{
  "url": "http://localhost:9200",
  "data": {
    "index": "airQuality",
    "id": "1"
  }
}'
# Update example
curl -X POST http://localhost:5000/update -H "Content-Type: application/json" -d '{
  "url": "http://localhost:9200",
  "data": {
    "index": "airQuality",
    "id": "1",
    "doc": {
      "BPM2_5": 56.78,
      "datetime_local": "2023-01-01-13",
      "location_name": "Los Angeles"
    }
  }
}'
# Read example (in case you really needed for no reason)
curl -X POST http://localhost:5000/read -H "Content-Type: application/json" -d '{
  "url": "http://localhost:9200",
  "data": {
    "index": "airQuality",
    "id": "1"
  }
}'

