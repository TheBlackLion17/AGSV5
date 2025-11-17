from pyrogram import Client, filters
from utils.keyboards import seasons_keyboard, episodes_keyboard
from database.database import db

db = MediaDB()

def register_season_handlers(app: Client):

    @app.on_callback_query(filters.regex(r"^open_seasons_"))
    async def open_seasons_handler(client, callback):
        file_id = callback.data.split("_")[2]
        seasons = await db.get_seasons(file_id)

        if not seasons:
            return await callback.answer("No seasons found.", show_alert=True)

        await callback.message.edit(
            "Select a Season:",
            reply_markup=seasons_keyboard(seasons, file_id)
        )

    @app.on_callback_query(filters.regex(r"^open_episodes_"))
    async def open_episodes_handler(client, callback):
        _, _, file_id, season = callback.data.split("_")

        episodes = await db.get_episodes(file_id, season)
        if not episodes:
            return await callback.answer("No episodes found.", show_alert=True)

        await callback.message.edit(
            f"Season {season} Episodes:",
            reply_markup=episodes_keyboard(episodes, file_id)
        )

    @app.on_callback_query(filters.regex(r"^back_to_seasons_"))
    async def back_to_seasons_handler(client, callback):
        file_id = callback.data.split("_")[3]
        seasons = await db.get_seasons(file_id)

        await callback.message.edit(
            "Select a Season:",
            reply_markup=seasons_keyboard(seasons, file_id)
        )
