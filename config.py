from dotenv import load_dotenv
import os

load_dotenv()

API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "SeriesDB")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "series")

# comma-separated list of Telegram user ids who are admins
ADMINS = [int(x.strip()) for x in os.getenv("ADMINS", "").split(",") if x.strip()]

# Channel IDs to auto-index (channel username or ID)
AUTOINDEX_CHANNELS = [x.strip() for x in os.getenv("AUTOINDEX_CHANNELS", "").split(",") if x.strip()]

POSTER_PLACEHOLDER = os.getenv("POSTER_PLACEHOLDER", "https://i.ibb.co/album-placeholder.png")

# Other options
FILE_CACHE_TTL = int(os.getenv("FILE_CACHE_TTL", "86400"))  # seconds
LOGS_COLLECTION = os.getenv("LOGS_COLLECTION", "user_logs")

LOG_CHANNEL = -1001234567890   # your log channel ID
BOT_NAME = "Series AutoFilter Bot"
