import asyncio
from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN
from database.mongodb import ensure_indexes
from plugins import indexer, search, handlers, admin

app = Client('series_bot', api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


@app.on_connect()
async def on_connect(client):
    await ensure_indexes()


async def main():
    # register modules
    await indexer.register_indexer(app)
    await search.register_search(app)
    await handlers.register_handlers(app)
    await admin.register_admin(app)
    await app.start()
    print('Bot started')
    await idle()

if __name__ == '__main__':
    asyncio.run(main())
