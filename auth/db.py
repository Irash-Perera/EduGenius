from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Connect to the MongoDB database
try:
    client = MongoClient("REMOVED_SECRET")
    db = client["EduGenius"]
    collection = db["Users"]
except Exception as e:
    print(e)