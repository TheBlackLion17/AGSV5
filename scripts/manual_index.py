

import asyncio
from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN, DUMP_CHANNELS
from database.mongodb import media_col
from utils.helpers import parse_filename

app = Client('indexer', api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

async def run():
    async with app:
        channels = [c.strip() for c in DUMP_CHANNELS.split(',') if c.strip()]
        for ch in channels:
            async for msg in app.get_chat_history(ch, limit=10000):
                if msg.document or msg.video or msg.animation:
                    media = msg.document or msg.video or msg.animation
                    file_id = media.file_id
                    title = (msg.caption or media.file_name or 'untitled').strip()
                    parsed = parse_filename(title)
                    doc = {
                        'chat_id': msg.chat.id,
                        'message_id': msg.message_id,
                        'file_id': file_id,
                        'title': title,
                        'series': parsed.get('series'),
                        'season': parsed.get('season'),
                        'episode': parsed.get('episode')
                    }
                    await media_col.update_one({'chat_id': doc['chat_id'], 'message_id': doc['message_id']}, {'$set': doc}, upsert=True)
                    print('Indexed', title)

if __name__ == '__main__':
    asyncio.run(run())
