import asyncio
from datetime import datetime
from aiohttp import web
from pyrogram import Client, idle

# Config
from config import (
    API_ID,
    API_HASH,
    BOT_TOKEN,
    LOG_CHANNEL,
    BOT_NAME,
    PORT         # <-- Added PORT support
)

# Handlers
from handlers.search import register_search_handlers
from handlers.season import register_season_handlers
from handlers.quality import register_quality_handlers
from handlers.index import register_autoindex_handlers
from handlers.admin import register_admin_handlers
from handlers.file_cache import register_filecache_handlers
from handlers.user_logs import register_userlog_handlers

# Script (messages)
from script import *


# ---------------------------------------------------------------------------
# SIMPLE WEB SERVER (Render / Railway / Koyeb / Heroku support)
# ---------------------------------------------------------------------------
async def web_index(request):
    return web.Response(text=f"{BOT_NAME} is running successfully ✔️")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", web_index)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()
    print(f"🌍 Web server running on port {PORT}")


# ---------------------------------------------------------------------------
# SEND STARTUP LOG
# ---------------------------------------------------------------------------
async def send_startup_log(app: Client):
    """Send bot online notification to the log channel."""
    try:
        await app.send_message(
            LOG_CHANNEL,
            LOG_MSG.format(
                bot_name=BOT_NAME,
                time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
        )
    except Exception as error:
        print(f"[Startup-Log] Failed to send log: {error}")


# ---------------------------------------------------------------------------
# MAIN BOT LAUNCHER
# ---------------------------------------------------------------------------
def main():

    # Initialize bot session
    app = Client(
        "AutoFilterBot",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN
    )

    # Register handlers
    register_search_handlers(app)
    register_season_handlers(app)
    register_quality_handlers(app)
    register_autoindex_handlers(app)
    register_admin_handlers(app)
    register_filecache_handlers(app)
    register_userlog_handlers(app)

    # Start bot
    app.start()
    print("⚡ Bot Started Successfully")

    # Send bot online log
    app.loop.run_until_complete(send_startup_log(app))

    # Start Web Server in background
    app.loop.create_task(start_web_server())

    # Keep bot running
    idle()

    # Stop bot on close
    app.stop()
    print("🛑 Bot Stopped")


# ---------------------------------------------------------------------------
# RUN BOT
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    main()
