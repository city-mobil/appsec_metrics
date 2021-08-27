from pymongo import MongoClient
from config import config
import os
import urllib.parse

def upload_to_mongodb(timeline, db, coolections):
    client = MongoClient(os.environ.get('mongodb_connect_string'))
    db = client[db]
    mongo_timeline_collection = db[coolections]
    mongo_timeline_collection.delete_many({})
    mongo_timeline_collection.insert_many(timeline)


    return None

if __name__ == '__main__':
    upload_to_mongodb(None,'wrt','wrt')