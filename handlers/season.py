from pyrogram import Client, filters
from pyrogram.types import Message
from utils.keyboards import episodes_keyboard
from database import MediaDB

db = MediaDB()

def register_season_handlers(app: Client):

    @app.on_callback_query(filters.regex(r"^season_\d+_"))
    async def season_handler(client, callback):
        data = callback.data.split("_")
        _, season, file_id = data  # season_1_12345

        episodes = await db.get_episodes(file_id, season)
        if not episodes:
            return await callback.message.edit(
                f"No episodes found for Season {season}."
            )

        await callback.message.edit(
            f"Season {season} Episodes:",
            reply_markup=episodes_keyboard(episodes, file_id)
        )
