from pymongo import MongoClient
from config import MONGO_URI, DB_NAME, COLLECTION_NAME, LOGS_COLLECTION
from bson import ObjectId

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]
logs = db[LOGS_COLLECTION]

# Series helper
def search_series(query):
    return collection.find_one({"title": {"$regex": query, "$options": "i"}})

def get_series_by_id(object_id):
    try:
        return collection.find_one({"_id": ObjectId(object_id)})
    except Exception:
        return None

def insert_or_update_series(series_doc):
    # series_doc should contain a unique 'title' (case-insensitive)
    existing = collection.find_one({"title": {"$regex": f"^{series_doc['title']}$", "$options": "i"}})
    if existing:
        # update fields (merge seasons etc.)
        collection.update_one({"_id": existing["_id"]}, {"$set": series_doc})
        return existing["_id"]
    else:
        return collection.insert_one(series_doc).inserted_id

# Logs
def log_user_action(user_id, username, action, meta=None):
    logs.insert_one({
        "user_id": user_id,
        "username": username,
        "action": action,
        "meta": meta or {},
        "ts": __import__('datetime').datetime.utcnow()
    })

# Simple stats
def get_stats():
    return {
        "series_count": collection.count_documents({}),
        "logs_count": logs.count_documents({})
    }
