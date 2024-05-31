#!/bin/sh

# check if route name is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <route_name>"
  exit 1
fi

ROUTE_NAME=$1
BASE_URL="http://127.0.0.1:9090"

# construct the URL
URL="${BASE_URL}/${ROUTE_NAME}"

# send a GET request to the URL
curl "$URL" | jq '.'

# check if the request was successful
if [ $? -ne 0 ]; then
  echo "Error: Failed to retrieve data from $URL"
  exit 1
fi

echo "Data successfully retrieved from $URL"
