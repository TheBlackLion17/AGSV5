from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.database import search_series, get_series_by_id, log_user_action
from utils.keyboards import seasons_keyboard
from utils.logger import logger
from config import POSTER_PLACEHOLDER, DEFAULT_SEARCH_LIMIT


def register_search_handlers(app):

    @app.on_message(filters.text & ~filters.command(["start", "help"]))
    async def search_handler(client, message):
        query = message.text.strip()

        logger.info(f"Search request: {query} by {message.from_user.id}")
        log_user_action(
            message.from_user.id,
            getattr(message.from_user, "username", None),
            "search",
            {"query": query}
        )

        results = search_series(query, limit=DEFAULT_SEARCH_LIMIT)

        if not results:
            await message.reply_text("❌ No results found.")
            return

        # If only one result — show full details
        if len(results) == 1:
            r = results[0]

            caption = (
                f"📺 **Title:** {r.get('title')} \n"
                f"📅 **Released:** {r.get('released', 'N/A')} \n"
                f"🎭 **Genre:** {r.get('genre', 'N/A')} \n"
                f"⭐ **Rating:** {r.get('rating', 'N/A')} \n"
            )

            await message.reply_photo(
                photo=r.get("poster", POSTER_PLACEHOLDER),
                caption=caption,
                reply_markup=seasons_keyboard(r)
            )
            return

        # Multiple results: send list
        text = "🔍 **Multiple results found:**\n\n"
        buttons = []

        for r in results:
            text += f"• {r.get('title')}\n"
            buttons.append([
                InlineKeyboardButton(
                    r.get("title"),
                    callback_data=f"pick_{r['_id']}"
                )
            ])

        await message.reply_text(
            text,
            reply_markup=InlineKeyboardMarkup(buttons)
        )
