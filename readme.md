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