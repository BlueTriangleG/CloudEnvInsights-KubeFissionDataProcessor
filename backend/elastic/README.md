# FILE STRUCTURE
### ./mapping
for all mappings and initialisations
### ./crud
for create delete read and update basic methods
### ./querying
for advanced query operations including merging ability
### ./utils
for flask router and helper functions
### ./example
teacher's test example for localhost elastic search

# CREATE INDEX (INITIALISATION)
### main() have been implemented so that you can directly fission it by:
fission function update --name create_indexes --env python --code <genshin!>_mapping.py --method POST
### using by post and passing context like this: (change it to real API)
{"url": "http://local-elasticsearch:9200"}
### whole POST command example here!
curl -X POST http://$FISSION_ROUTER/create-<what>-index -H "Content-Type: application/json" -d '{"url": "http://local-elasticsearch:9200"}'

# USE CRUD
### Create example
curl -X POST http://localhost:5000/create -H "Content-Type: application/json" -d '{
  "url": "http://localhost:9200",
  "data": {
    "index": "airQuality",
    "BPM2_5": 12.34,
    "datetime_local": "2023-01-01-12",
    "location_name": "San Francisco"
  }
}'
### Delete example
curl -X POST http://localhost:5000/delete -H "Content-Type: application/json" -d '{
  "url": "http://localhost:9200",
  "data": {
    "index": "airQuality",
    "id": "1"
  }
}'
### Update example
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
### Read example (in case you really needed for no reason)
curl -X POST http://localhost:5000/read -H "Content-Type: application/json" -d '{
  "url": "http://localhost:9200",
  "data": {
    "index": "airQuality",
    "id": "1"
  }
}'

# FULL INSTRUCTION FOR FISSION
### Deployment for router application
fission environment create --name python --image fission/python-env
fission function create --name elastic-functions --env python --code app.py
fission route create --method POST --url /create --function elastic-functions
fission route create --method POST --url /read --function elastic-functions
fission route create --method POST --url /update --function elastic-functions
fission route create --method POST --url /delete --function elastic-functions
fission route create --method POST --url /create-air-quality-index --function elastic-functions
fission route create --method POST --url /create-weather-index --function elastic-functions
### Make command scriptable(/create example)
curl script(e.g. invoke_create.sh):
    #!/bin/bash
    # Fission Router IP and Port
    FISSION_ROUTER_IP="<FISSION_ROUTER_IP>"
    PORT="<PORT>"
    # Fetch data from the data source
    DATA=$(curl -s $DATA_SOURCE_URL)
    # cURL command to invoke /create endpoint with the read data
    curl -X POST http://$FISSION_ROUTER_IP:$PORT/create -H "Content-Type: application/json" -d "$DATA"
where $DATA is your environment getable json from $DATA_SOURCE_URL
### Deployment scriptsh
tar -cvf invoke_create.tar invoke_create.sh
fission function create --name invoke-create --env binary --deploy invoke_create.tar --entrypoint "/bin/bash invoke_create.sh"
### Trigger(timer example)
fission timer create --name periodic-invoke-create --cron "@every 1h" --function invoke-create


