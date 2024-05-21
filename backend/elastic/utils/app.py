from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch

app = Flask(__name__)

from crud.elasticCreate import create_handler
from crud.elasticRead import read_handler
from crud.elasticDelete import delete_handler
from crud.elasticUpdate import update_handler

from mapping.airQuality_mapping import create_air_quality_index
from mapping.weather_mapping import create_weather_index

@app.route('/create', methods=['POST'])
def create():
    req = request.json
    result = create_handler(req)
    return jsonify(result)

@app.route('/read', methods=['POST'])
def read():
    req = request.json
    result = read_handler(req)
    return jsonify(result)

@app.route('/update', methods=['POST'])
def update():
    req = request.json
    result = update_handler(req)
    return jsonify(result)

@app.route('/delete', methods=['POST'])
def delete():
    req = request.json
    result = delete_handler(req)
    return jsonify(result)

@app.route('/create-air-quality-index', methods=['POST'])
def create_air_quality_index_route():
    req = request.get_json()
    result = create_air_quality_index(req)
    return jsonify(result)

@app.route('/create-weather-index', methods=['POST'])
def create_weather_index_route():
    req = request.get_json()
    result = create_weather_index(req)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)


