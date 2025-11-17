from pyrogram import filters
from utils.keyboards import make_quality_buttons
from database.database import get_series_by_id, log_user_action
from utils.logger import logger


def season_handlers(bot):

    @bot.on_callback_query(filters.regex(r"^season_"))
    async def season_menu(client, query):
        try:
            _, item_id, season_no = query.data.split("_")
        except:
            await query.answer("Invalid data", show_alert=True)
            return

        logger.info(f"Season selected: {item_id} s{season_no}")

        item = get_series_by_id(item_id)
        if not item:
            await query.answer("Item not found", show_alert=True)
            return

        # find season
        selected = next(
            (s for s in item.get("seasons", []) if str(s.get("season_no")) == str(season_no)),
            None
        )

        if not selected:
            await query.answer("Season not found", show_alert=True)
            return

        qualities = list(selected.get("quality", {}).keys())
        markup = make_quality_buttons(item_id, season_no, qualities)

        await query.message.edit_caption(
            f"""🎬 **{item['title']}**
📌 Select quality for **Season {season_no}**""",
            reply_markup=markup
        )

        log_user_action(
            query.from_user.id,
            getattr(query.from_user, "username", None),
            "select_season",
            {"item_id": item_id, "season": season_no},
        )

        await query.answer()
