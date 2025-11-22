from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URI

_client = AsyncIOMotorClient(MONGO_URI)
_db = _client['series_sharing']

media_col = _db['media']
settings_col = _db['settings']
users_col = _db['users']

async def ensure_indexes():
    await media_col.create_index([('title', 'text'), ('tags', 'text')])
    await media_col.create_index('message_id')
    await users_col.create_index('user_id', unique=True)
