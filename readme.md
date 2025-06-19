### Architecture 

```
cqrs/
├── docker-compose.yml
├── README.md

├── api-write/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── db.py
│   ├── kafka_producer.py
│   ├── models.py
│   └── main.py

├── api-read/
│   ├── Dockerfile
│   └── requirements.txt

├── sync-worker/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── sql_mapper.py
│   └── worker.py
```

#### FAIRE UNE INSERTION 
```bash
curl -X POST http://localhost:8001/commande \
-H "Content-Type: application/json" \
-d '{
  "client_id": "456",
  "produits": [
    {
      "produit_id": "2",
      "nom": "Souris",
      "quantite": 1
    }
  ],
  "total": 39.99
}'
```

#### CHECK MYSQL :
> docker exec -it mysql mysql -uroot -p
> root 
> SELECT * FROM techshop.commandes;
> SELECT * FROM techshop.lignes_commande;

#### CHECK MONGO DB :
> docker exec -it mongo mongosh
> use techshop
> db.commandes.find().pretty()

