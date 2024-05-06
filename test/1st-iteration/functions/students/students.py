from flask import request, current_app
import requests, logging, json

def main():

    current_app.logger.debug(f'Received request: {request.method}')
    return 'students', 200
