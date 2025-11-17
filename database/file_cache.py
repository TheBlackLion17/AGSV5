from pymongo import ASCENDING
from config import FILE_CACHE_TTL
from database.database import db
import time

cache = db['file_cache']
cache.create_index([('ts', ASCENDING)])

def put_file(key, file_id):
    cache.update_one(
        {'key': key},
        {'$set': {'file_id': file_id, 'ts': int(time.time())}},
        upsert=True
    )

def get_file(key):
    r = cache.find_one({'key': key})
    if not r:
        return None
    if int(time.time()) - r['ts'] > FILE_CACHE_TTL:
        cache.delete_one({'key': key})
        return None
    return r['file_id']
