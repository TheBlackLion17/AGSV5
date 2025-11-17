from pyrogram import filters
from database.database import get_stats, log_user_action, collection
from config import ADMINS
from utils.logger import logger


def admin_handlers(bot):
    # /stats
    @bot.on_message(filters.command(["stats"]) & filters.user(ADMINS))
    async def cmd_stats(client, message):
        stats = get_stats()
        await message.reply(f"Series: {stats['series_count']}")
Logs: (stats['logs_count'])")

    # /broadcast <text>
    @bot.on_message(filters.command(["broadcast"]) & filters.user(ADMINS))
    async def cmd_broadcast(client, message):
        if len(message.command) < 2:
            await message.reply("Usage: /broadcast Your message here")
            return
        text = message.text.split(None, 1)[1]
        # naive broadcast to all users in logs (unique)
        user_ids = collection.database[ 'user_logs' ].distinct('user_id')
        sent = 0
        for uid in user_ids:
            try:
                await client.send_message(uid, text)
                sent += 1
            except Exception as e:
                logger.warning(f"Failed to send to {uid}: {e}")
        await message.reply(f"Broadcast sent to {sent} users")

    # /addseries (admin only) - supply JSON in reply to message
    @bot.on_message(filters.command(["addseries"]) & filters.user(ADMINS))
    async def cmd_addseries(client, message):
        # expects a JSON payload in reply or message
        import json
        payload = None
        if message.reply_to_message and message.reply_to_message.text:
            payload = message.reply_to_message.text
        elif len(message.command) > 1:
            payload = message.text.split(None,1)[1]
        if not payload:
            await message.reply("Please provide a series JSON in message or reply")
            return
        try:
            doc = json.loads(payload)
            from database import insert_or_update_series
            _id = insert_or_update_series(doc)
            await message.reply(f"Series inserted/updated: {_id}")
        except Exception as e:
            await message.reply(f"Failed to parse/insert JSON: {e}")
