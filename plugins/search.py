from pyrogram import filters
from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent
from database.mongodb import media_col
from utils.keyboards import media_result_buttons
from bson.objectid import ObjectId

async def register_search(app):
    @app.on_inline_query()
    async def inline_search(client, inline_query):
        q = inline_query.query.strip()
        if not q:
            return await inline_query.answer([], cache_time=1)
        # text search
        cursor = media_col.find({'$text': {'$search': q}}).limit(20)
        results = []
        async for doc in cursor:
            rid = str(doc['_id'])
            title = doc.get('title', 'untitled')
            thumb = doc.get('poster_file_id')
            input_msg = InputTextMessageContent(f"Found: {title}\nSeries: {doc.get('series')}")
            res = InlineQueryResultArticle(
                id=rid,
                title=title[:64],
                input_message_content=input_msg,
            )
            results.append(res)
        await inline_query.answer(results)
