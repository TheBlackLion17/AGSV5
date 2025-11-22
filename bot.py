import asyncio
from pyrogram import Client, idle
from config import API_ID, API_HASH, BOT_TOKEN
from database.mongodb import ensure_indexes
from plugins import indexer, search, handlers, admin

app = Client(
    "series_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

async def main():

    # Start the bot first
    await app.start()
    print("Bot connected!")

    # Run your startup tasks here instead of on_connect()
    await ensure_indexes()

    # Register modules AFTER bot started
    await indexer.register_indexer(app)
    await search.register_search(app)
    await handlers.register_handlers(app)
    await admin.register_admin(app)

    print("Bot started successfully!")
    await idle()

if __name__ == "__main__":
    asyncio.run(main())
