import asyncio
from datetime import datetime
from pyrogram import Client, idle
from config import API_ID, API_HASH, BOT_TOKEN, LOG_CHANNEL, BOT_NAME

# Handlers
from handlers.search import register_search_handlers
from handlers.season import register_season_handlers
from handlers.quality import register_quality_handlers
from handlers.autoindex import register_autoindex_handlers
from handlers.admin import register_admin_handlers
from handlers.file_cache import register_filecache_handlers
from handlers.user_logs import register_userlog_handlers


# ----------------------------------------------------------------
# STARTUP LOG MESSAGE
# ----------------------------------------------------------------
async def send_startup_log(app: Client):
    """Send bot-online message to the log channel."""
    try:
        await app.send_message(chat_id=LOG_CHANNEL, text=script)
    except Exception as error:
        print(f"[Startup-Log] Failed to send log: {error}")


# ----------------------------------------------------------------
# MAIN FUNCTION
# ----------------------------------------------------------------
def main():
    app = Client(
        "autofilter-bot",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN
    )

    # ----------------------------
    # REGISTER ALL HANDLERS
    # ----------------------------
    register_search_handlers(app)
    register_season_handlers(app)
    register_quality_handlers(app)
    register_autoindex_handlers(app)
    register_admin_handlers(app)
    register_filecache_handlers(app)
    register_userlog_handlers(app)

    # ----------------------------
    # START BOT
    # ----------------------------
    app.start()
    print("⚡ Bot Started Successfully")

    # Send startup status to log channel
    app.loop.run_until_complete(send_startup_log(app))

    # Keep bot running
    idle()

    # Stop safely
    app.stop()
    print("🛑 Bot Stopped")


# ----------------------------------------------------------------
# EXECUTION
# ----------------------------------------------------------------
if __name__ == "__main__":
    main()
