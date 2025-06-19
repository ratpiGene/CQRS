from fastapi import FastAPI
from models import Commande
from db import commandes_collection
from kafka_producer import envoyer_evenement

app = FastAPI()

@app.post("/commande")
def creer_commande(commande: Commande):
    doc = commande.dict()
    res = commandes_collection.insert_one(doc)
    envoyer_evenement("commande_created", { "id": str(res.inserted_id), **doc })
    return { "status": "ok", "id": str(res.inserted_id) }
