from kafka import KafkaConsumer
import json
import mysql.connector
import os
from sql_mapper import insert_commande

KAFKA_SERVER = os.getenv("KAFKA_SERVER", "kafka:9092")
TOPIC = "commande_created"

# Connexion MySQL
conn = mysql.connector.connect(
    host=os.getenv("MYSQL_HOST", "mysql"),
    user=os.getenv("MYSQL_USER", "root"),
    password=os.getenv("MYSQL_PASSWORD", "root"),
    database=os.getenv("MYSQL_DB", "techshop")
)
cursor = conn.cursor()

# Kafka Consumer
consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=KAFKA_SERVER,
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    auto_offset_reset='earliest',
    enable_auto_commit=True
)

print("Sync-worker listening to Kafka...")

for message in consumer:
    commande = message.value
    print("📥 Commande reçue :", commande)
    insert_commande(cursor, commande)
    conn.commit()
