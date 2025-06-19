from kafka import KafkaProducer
import json
import os

KAFKA_SERVER = os.getenv("KAFKA_SERVER", "kafka:9092")
KAFKA_SERVER = KAFKA_SERVER.replace(" ", "")

producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    retries=5  # Recommandé pour éviter les crashs immédiats
)

def envoyer_evenement(topic, message: dict):
    producer.send(topic, message)
    producer.flush()
