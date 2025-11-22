from pyrogram import Client, filters
from config import DUMP_CHANNELS, ADMINS
from database.mongodb import media_col
from utils.helpers import parse_filename
from models.media_model import MediaItem

# This module registers a handler that listens to messages in configured dump channels

async def register_indexer(app: Client):
    channels = [c.strip() for c in DUMP_CHANNELS.split(',') if c.strip()]

    @app.on_message(filters.chat(channels) & (filters.video | filters.document | filters.animation))
    async def auto_index(client, message):
        # only index new messages
        try:
            media = message.document or message.video or message.animation
            file_id = media.file_id
            title = (message.caption or media.file_name or 'untitled').strip()
            parsed = parse_filename(title)
            item = MediaItem(
                message_id=message.message_id,
                chat_id=message.chat.id,
                file_id=file_id,
                title=title,
                series=parsed.get('series'),
                season=parsed.get('season'),
                episode=parsed.get('episode'),
                quality=None,
                language=None,
                poster_file_id=None,
                tags=[]
            )
            await media_col.update_one(
                {'chat_id': item.chat_id, 'message_id': item.message_id},
                {'$set': item.to_dict()}, upsert=True)
            # optional: notify admins when new media is indexed
            for a in ADMINS:
                try:
                    await client.send_message(a, f'Indexed: {title} (id {message.message_id})')
                except Exception:
                    pass
        except Exception as e:
            print('Index error', e)

