from pyrogram import filters
from database.database import insert_or_update_series, log_user_action
from config import AUTOINDEX_CHANNELS
from utils.logger import logger


def autoindex_handlers(bot):

    @bot.on_message(filters.channel & filters.incoming)
    async def channel_watcher(client, message):

        chat = message.chat
        channel_list = [c.lower().lstrip('@') for c in AUTOINDEX_CHANNELS]

        # Match by username (e.g. @MyChannel)
        if chat.username and chat.username.lower() in channel_list:
            await _index_message(message)

        # Match by channel ID
        elif str(chat.id) in AUTOINDEX_CHANNELS:
            await _index_message(message)


    async def _index_message(message):

        # Extract title
        title = None

        if message.caption:
            title = message.caption.split("\n")[0].strip()

        elif message.document:
            title = message.document.file_name.rsplit(".", 1)[0]

        if not title:
            logger.info("Skipping message without title")
            return

        # Prepare quality dictionary
        quality_dict = {}

        if message.document:
            quality_dict["file"] = message.document.file_id

        # Build document
        doc = {
            "title": title,
            "poster": None,
            "seasons": [
                {
                    "season_no": 1,
                    "quality": quality_dict
                }
            ]
        }

        try:
            _id = insert_or_update_series(doc)
            log_user_action(
                message.from_user.id if message.from_user else 0,
                getattr(message.from_user, 'username', None),
                "autoindex",
                {"_id": str(_id), "title": title}
            )
            logger.info(f"Indexed: {title} -> {_id}")

        except Exception as e:
            logger.exception(f"Failed to index: {e}")
