# app/db.py
from pymongo import MongoClient
from app.config import load_env

config = load_env()
MONGO_URI = config['MONGO_URI']

client = MongoClient(MONGO_URI)
db = client['wagerDev']
user_collection = db['userTable']
match_collection = db['matchTable']

def get_db_client():
    return client