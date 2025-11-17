from pyrogram import filters
from utils.logger import logger
from database.file_cache import put_file, get_file


def register_filecache_handlers(bot):

    # Save every document the bot sees
    @bot.on_message(filters.document)
    async def cache_file(client, message):
        key = message.document.file_unique_id      # unique cache key
        file_id = message.document.file_id

        put_file(key, file_id)

        logger.info(f"[CACHE] Stored file: {key}")
        await message.reply(f"✅ Cached file!\nCache Key: `{key}`")

    # Retrieve a cached file via button
    @bot.on_callback_query(filters.regex(r"^cache_"))
    async def send_cached(client, query):
        key = query.data.split("_", 1)[1]

        file_id = get_file(key)
        if not file_id:
            await query.answer("❌ File expired or not found!", show_alert=True)
            return

        try:
            await query.message.reply_document(
                document=file_id,
                caption=f"📁 Cached File\nKey: `{key}`"
            )
            await query.answer("✔ Sent from cache!")
        except Exception as e:
            logger.error(f"Failed to send cached file: {e}")
            await query.message.reply("❌ Failed to send cached file.")
