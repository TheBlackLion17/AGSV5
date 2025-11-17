import asyncio
from datetime import datetime
from aiohttp import web
from pyrogram import Client, idle

from config import API_ID, API_HASH, BOT_TOKEN, LOG_CHANNEL, BOT_NAME, PORT, SESSION
from handlers.search import register_search_handlers
from handlers.season import register_season_handlers
from handlers.quality import register_quality_handlers
from handlers.index import register_autoindex_handlers
from handlers.admin import register_admin_handlers
from handlers.file_cache import register_filecache_handlers
from handlers.user_logs import register_userlog_handlers
from Script import script

# --------------------------
# Global app variable
# --------------------------
app = Client(
    name=SESSION,
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=50,
    plugins={"root": "handlers"},
    sleep_threshold=5
)

# --------------------------
# Web server
# --------------------------
async def web_index(request):
    return web.Response(text=f"{BOT_NAME} is running successfully ✔️")

async def start_web_server():
    web_app = web.Application()
    web_app.router.add_get("/", web_index)
    runner = web.AppRunner(web_app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()
    print(f"🌍 Web server running on port {PORT}")

# --------------------------
# Send startup log
# --------------------------
async def send_startup_log():
    today = datetime.now().strftime("%Y-%m-%d")
    time = datetime.now().strftime("%H:%M:%S")
    try:
        await app.send_message(
            chat_id=LOG_CHANNEL,
            text=script.RESTART_GC_TXT.format(today=today, time=time)
        )
    except Exception as e:
        print(f"[Startup-Log] Failed: {e}")

# --------------------------
# Register handlers
# --------------------------
def register_handlers():
    register_search_handlers(app)
    register_season_handlers(app)
    register_quality_handlers(app)
    register_autoindex_handlers(app)
    register_admin_handlers(app)
    register_filecache_handlers(app)
    register_userlog_handlers(app)

# --------------------------
# Main launcher
# --------------------------
async def main():
    # Register handlers
    register_handlers()

    # Start bot
    await app.start()
    print("⚡ Bot Started Successfully")

    # Send startup log
    await send_startup_log()

    # Start web server
    asyncio.create_task(start_web_server())

    # Keep bot running
    await idle()

    # Stop bot on shutdown
    await app.stop()
    print("🛑 Bot Stopped")

# --------------------------
# Run
# --------------------------
if __name__ == "__main__":
    asyncio.run(main())
