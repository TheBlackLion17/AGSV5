from dotenv import load_dotenv
import os

load_dotenv()

API_ID = int(os.getenv("API_ID", "20919286"))
API_HASH = os.getenv("API_HASH", "57b85f72104db3f08f9795b0410eb556")
BOT_TOKEN = os.getenv("BOT_TOKEN", "8348783837:AAHGHlZLej61NVYMGiEJcLaa6k6ouLRiIkE")

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://akku:akku@cluster0.7smnpac.mongodb.net/?appName=Cluster0")
DB_NAME = os.getenv("DB_NAME", "cluster0")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "series")

# comma-separated list of Telegram user ids who are admins
ADMINS = [int(x.strip()) for x in os.getenv("ADMINS", "7705748477").split(",") if x.strip()]

# Channel IDs to auto-index (channel username or ID)
AUTOINDEX_CHANNELS = [x.strip() for x in os.getenv("AUTOINDEX_CHANNELS", "-1002518840015").split(",") if x.strip()]

POSTER_PLACEHOLDER = os.getenv("POSTER_PLACEHOLDER", "https://i.ibb.co/album-placeholder.png")

# Other options
FILE_CACHE_TTL = int(os.getenv("FILE_CACHE_TTL", "86400"))  # seconds
LOGS_COLLECTION = os.getenv("LOGS_COLLECTION", "user_logs")

LOG_CHANNEL = -1002801544620   # your log channel ID
BOT_NAME = "agsfilterV3_bot"

# Default number of search results to show
DEFAULT_SEARCH_LIMIT = 10
