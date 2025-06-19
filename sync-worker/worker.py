from kafka import KafkaConsumer
import json
import mysql.connector
import time
import os
from sql_mapper import insert_commande

KAFKA_SERVER = os.getenv("KAFKA_SERVER", "kafka:9092")
KAFKA_SERVER = KAFKA_SERVER.replace(" ", "")
TOPIC = "commande_created"

# 🔁 Connexion MySQL avec retry
def connect_to_mysql(max_retries=5, delay=5):
    for i in range(max_retries):
        try:
            conn = mysql.connector.connect(
                host=os.getenv("MYSQL_HOST", "mysql"),
                user=os.getenv("MYSQL_USER", "root"),
                password=os.getenv("MYSQL_PASSWORD", "root"),
                database=os.getenv("MYSQL_DB", "techshop")
            )
            print("✅ Connexion MySQL réussie.")
            return conn
        except Exception as e:
            print(f"❌ Tentative {i+1}/{max_retries} : échec connexion MySQL → {e}")
            time.sleep(delay)
    raise RuntimeError("⛔ Impossible de se connecter à MySQL après plusieurs tentatives.")

def init_db(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS commandes (
            commande_id VARCHAR(255) PRIMARY KEY,
            client_id VARCHAR(255),
            total DECIMAL(10, 2)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lignes_commande (
            id INT AUTO_INCREMENT PRIMARY KEY,
            commande_id VARCHAR(255),
            produit_id VARCHAR(255),
            quantite INT,
            FOREIGN KEY (commande_id) REFERENCES commandes(commande_id)
        )
    """)
    print("✅ Tables MySQL vérifiées / créées.")

# Démarrage
conn = connect_to_mysql()
cursor = conn.cursor()
init_db(cursor)

# Kafka Consumer
consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=KAFKA_SERVER,
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='sync-worker-group',
    consumer_timeout_ms=10000
)

print("🔄 Sync-worker en écoute sur Kafka...")

for message in consumer:
    commande = message.value
    print("📥 Commande reçue :", commande)
    insert_commande(cursor, commande)
    conn.commit()
