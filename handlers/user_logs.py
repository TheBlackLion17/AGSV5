from pyrogram import filters
from utils.logger import logger
from database.database import log_user_action, db
from config import ADMINS


def register_userlog_handlers(bot):

    # Log all commands (valid commands start with /)
    @bot.on_message(filters.regex(r"^/"))
    async def log_commands(client, message):
        try:
            user_id = message.from_user.id
            username = message.from_user.username
            command = message.text.split()[0]

            log_user_action(
                user_id=user_id,
                username=username,
                action="command",
                details={"command": command}
            )

            logger.info(f"[LOG] User {user_id} used command: {command}")

        except Exception as e:
            logger.error(f"[LOG ERROR] {e}")

    # Log all callback button clicks
    @bot.on_callback_query()
    async def log_callbacks(client, query):
        try:
            user_id = query.from_user.id
            username = query.from_user.username
            data = query.data

            log_user_action(
                user_id=user_id,
                username=username,
                action="callback",
                details={"data": data}
            )

            logger.info(f"[LOG] User {user_id} pressed: {data}")

        except Exception as e:
            logger.error(f"[LOG ERROR] {e}")

    # /mylog
    @bot.on_message(filters.command("mylog"))
    async def my_logs(client, message):
        user_id = message.from_user.id
        logs = list(db["user_logs"].find({"user_id": user_id}).sort("ts", -1).limit(20))

        if not logs:
            await message.reply("📭 No logs found for you.")
            return

        text = "📘 **Your last logs:**\n\n"
        for l in logs:
            text += f"• {l.get('action')} — {l.get('details', {})}\n"

        await message.reply(text)

    # /logs (admin only)
    @bot.on_message(filters.command("logs") & filters.user(ADMINS))
    async def admin_logs(client, message):
        logs = list(db["user_logs"].find().sort("ts", -1).limit(30))

        if not logs:
            await message.reply("📭 No logs found.")
            return

        text = "📘 **Latest Logs:**\n\n"
        for l in logs:
            text += f"• User `{l.get('user_id')}` → {l.get('action')} — {l.get('details', {})}\n"

        await message.reply(text)
