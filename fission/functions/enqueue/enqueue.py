import logging, json, requests, socket
from flask import current_app, request
from aiokafka import AIOKafkaProducer
import asyncio

async def publish(queue, payload):
    producer = AIOKafkaProducer(bootstrap_servers='my-cluster-kafka-bootstrap.kafka.svc:9092')
    await producer.start()
    try:
        await producer.send_and_wait(queue, payload)
    finally:
        await producer.stop()

def main():
    asyncio.run (
        publish (
            request.headers.get('X-Fission-Params-Topic'),
            json.dumps(request.get_json()).encode('utf-8')
        )
    )
    current_app.logger.info(f'Enqueued to topic {request.headers.get("X-Fission-Params-Topic")}')
    return 'OK'
