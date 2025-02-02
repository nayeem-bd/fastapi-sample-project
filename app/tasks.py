from celery import Celery
import time
import pymongo
import os

REDIS_URI = os.getenv("REDIS_URI", "redis://redis:6379/0")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongodb:27017/")
MONGO_DB_NAME = os.getenv("MONGO_DB", "celery_db")

celery_app = Celery(
    "worker",
    broker=REDIS_URI,
    backend=MONGO_URI
)

# MongoDB client
client = pymongo.MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]
collection = db["task_results"]

@celery_app.task
def create_task(data):
    time.sleep(5)  # Simulate a long-running task
    result = {"data": data, "status": "completed"}
    collection.insert_one(result)
    return result
