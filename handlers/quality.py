from pyrogram import filters
from database import get_series_by_id, log_user_action
from utils.logger import logger


def quality_handlers(bot):
    @bot.on_callback_query(filters.regex(r"^quality_"))
    async def quality_send(client, query):
        _, item_id, season_no, quality = query.data.split("_")
        logger.info(f"Quality selected: {item_id} s{season_no} {quality}")
        item = get_series_by_id(item_id)
        if not item:
            await query.answer("Item not found", show_alert=True)
            return

        # Find the file link
        selected = next((s for s in item.get('seasons', []) if str(s.get('season_no')) == str(season_no)), None)
        if not selected:
            await query.answer("Season not found", show_alert=True)
            return

        file_link = selected.get('quality', {}).get(quality)
        if not file_link:
            await query.answer("File not found", show_alert=True)
            return

        # If file_link looks like a file_id string (tg:// or starts with 'AQ' etc.) we send document, otherwise send as url
        try:
            await query.message.reply_document(document=file_link, caption=f"🎬 **{item['title']}**
Season {season_no}
Quality: {quality}")
        except Exception:
            # fallback to sending as text link
            await query.message.reply_text(f"File: {file_link}")

        log_user_action(query.from_user.id, getattr(query.from_user, 'username', None), 'get_file', {'item_id': item_id, 'season': season_no, 'quality': quality})
        await query.answer(),
