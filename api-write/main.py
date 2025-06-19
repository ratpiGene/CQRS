from fastapi import FastAPI
from models import Commande
from db import commandes_collection
from kafka_producer import envoyer_evenement
from bson import ObjectId

app = FastAPI()

# ✅ Fonction récursive pour convertir tous les ObjectId en str
def convertir_objectid(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    elif isinstance(obj, dict):
        return {k: convertir_objectid(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convertir_objectid(i) for i in obj]
    else:
        return obj

@app.post("/commande")
def creer_commande(commande: Commande):
    doc = commande.dict()
    res = commandes_collection.insert_one(doc)

    payload = convertir_objectid({"id": res.inserted_id, **doc})  # ✅ conversion complète ici
    envoyer_evenement("commande_created", payload)

    return {"status": "ok", "id": str(res.inserted_id)}
