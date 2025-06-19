from kafka import KafkaProducer
import json
import os

KAFKA_SERVER = os.getenv("KAFKA_SERVER", "kafka:9092")

producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def envoyer_evenement(topic, message: dict):
    producer.send(topic, message)
    producer.flush()
