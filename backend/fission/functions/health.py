from flask import request, current_app
import requests, logging
import json

def main():
    # return a json file, content is 1
    r = {"value": 1}
    return json.dumps(r)
print(main())