import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import PyMongoError

load_dotenv()

_client=None
def init_db():
    global _client
    uri=os.getenv('MONGODB_URI','mongodb://127.0.0.1:27017/')
    name=os.getenv('MONGODB_DB','smart_parking_db')
    # BSON dates are stored as UTC. Return aware UTC datetimes so analytics
    # can safely compare them with timezone-aware reporting-window bounds.
    if _client is None: _client=MongoClient(uri, serverSelectionTimeoutMS=2500, tz_aware=True)
    db=_client[name]
    db.command('ping')
    return db

def get_db(): return init_db()
