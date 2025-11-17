from pyrogram import filters
from database.database import get_series_by_id, log_user_action
from utils.logger import logger


def register_quality_handlers(bot):
    @bot.on_callback_query(filters.regex(r"^quality_"))
    async def quality_send(client, query):
        """
        Callback data format:
        quality_{item_id}_{season_no}_{quality}
        """
        _, item_id, season_no, quality = query.data.split("_")
        logger.info(f"Quality selected: {item_id} s{season_no} {quality}")

        item = get_series_by_id(item_id)
        if not item:
            await query.answer("Item not found", show_alert=True)
            return

        # Find selected season
        selected = next(
            (s for s in item.get("seasons", [])
             if str(s.get("season_no")) == str(season_no)),
            None
        )

        if not selected:
            await query.answer("Season not found", show_alert=True)
            return

        # Get file link for this quality
        file_link = selected.get("quality", {}).get(quality)
        if not file_link:
            await query.answer("File not found", show_alert=True)
            return

        caption_text = (
            f"🎬 **{item['title']}**\n"
            f"📺 Season: {season_no}\n"
            f"🎚 Quality: {quality}"
        )

        # Try sending as Telegram file_id/document
        try:
            await query.message.reply_document(
                document=file_link,
                caption=caption_text
            )
        except Exception:
            # Fallback to sending URL or plain text
            await query.message.reply_text(f"File: {file_link}")

        # Log user action
        log_user_action(
            query.from_user.id,
            getattr(query.from_user, 'username', None),
            "get_file",
            {"item_id": item_id, "season": season_no, "quality": quality}
        )

        await query.answer("Sending…")
