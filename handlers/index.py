from pyrogram import filters
from database import insert_or_update_series, log_user_action
from config import AUTOINDEX_CHANNELS
from utils.logger import logger


def autoindex_handlers(bot):
    # Monitors configured channels for media/files and indexes them
    @bot.on_message(filters.channel & filters.incoming)
    async def channel_watcher(client, message):
        chat = message.chat
        if chat.username and chat.username.lower() in [c.lower().lstrip('@') for c in AUTOINDEX_CHANNELS]:
            await _index_message(message)
        elif str(chat.id) in AUTOINDEX_CHANNELS:
            await _index_message(message)

    async def _index_message(message):
        # Try to extract title from caption or filename
        title = None
        if message.caption:
            # crude: first line as title
            title = message.caption.split('
')[0].strip()
        elif message.document and message.document.file_name:
            title = message.document.file_name

        if not title:
            logger.info('Skipping message without title')
            return

        # Build series document (very simple schema)
        doc = {
            'title': title,
            'poster': None,
            'seasons': [
                {
                    'season_no': 1,
                    'quality': {
                        # store telegram file_id for document
                        message.document.file_name if message.document and message.document.file_name else 'file': message.document.file_id if message.document else None
                    }
                }
            ]
        }

        try:
            _id = insert_or_update_series(doc)
            log_user_action(message.from_user.id if message.from_user else 0, getattr(message.from_user, 'username', None), 'autoindex', {'_id': str(_id), 'title': title})
            logger.info(f"Indexed: {title} -> {_id}")
        except Exception as e:
            logger.exception(f"Failed to index: {e}")
