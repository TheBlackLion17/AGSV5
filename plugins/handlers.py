from pyrogram import filters
from pyrogram.types import CallbackQuery
from database.mongodb import media_col
from utils.keyboards import media_result_buttons, series_navigation_buttons
from bson.objectid import ObjectId

async def register_handlers(app):
    @app.on_callback_query()
    async def cb_handler(client, query: CallbackQuery):
        data = query.data
        if data.startswith('series_'):
            mid = data.split('_', 1)[1]
            doc = await media_col.find_one({'_id': ObjectId(mid)})
            if not doc:
                return await query.answer('Not found', show_alert=True)
            # show series overview with seasons
            series = doc.get('series') or doc.get('title')
            season = doc.get('season') or 1
            text = f"{series}\nSeason: {season}\nTitle: {doc.get('title')}"
            await query.message.edit_caption(text, reply_markup=series_navigation_buttons(series, season))
            await query.answer()

        elif data.startswith('send_'):
            mid = data.split('_', 1)[1]
            doc = await media_col.find_one({'_id': ObjectId(mid)})
            if not doc:
                return await query.answer('Not found', show_alert=True)
            # send file to user as a new message (works in PM)
            try:
                await client.copy_message(chat_id=query.from_user.id, from_chat_id=doc['chat_id'], message_id=doc['message_id'])
                await query.answer('Sent to your DM.')
            except Exception as e:
                await query.answer('Failed to send. Start the bot first (press Start).', show_alert=True)

        elif data.startswith('qualities|'):
            # data = qualities|{series_name}|{season}
            parts = data.split('|')
            _, series_name, season = parts
            season = int(season)
            # find available qualities for this series+season
            cursor = media_col.find({'series': series_name, 'season': season})
            qualities = {}
            async for d in cursor:
                q = d.get('quality') or 'unknown'
                key = f"{q} - E{d.get('episode')}"
                qualities.setdefault(q, []).append({'label': key, 'id': str(d['_id'])})
            # build buttons (first-quality example)
            if not qualities:
                return await query.answer('No episodes found for this season', show_alert=True)
            # flatten first quality
            first_q = next(iter(qualities))
            kb = []
            for ent in qualities[first_q][:12]:
                kb.append([InlineKeyboardButton(ent['label'], callback_data=f'send_{ent['id']}')])
            await query.message.edit_text(f'Quality: {first_q}\nChoose episode', reply_markup=make_paginated_buttons(qualities[first_q], 'send'))
            await query.answer()

        elif data.startswith('back_to_search'):
            await query.message.edit_text('Use inline search or type a query.')
            await query.answer()

    # handler for plain search in chat
    @app.on_message(filters.private & filters.text)
    async def chat_search(client, message):
        q = message.text.strip()
        if not q:
            return
        cursor = media_col.find({'$text': {'$search': q}}).limit(10)
        found = []
        async for doc in cursor:
            found.append(doc)
        if not found:
            return await message.reply('No results found')
        # send first 5 results as list
        for doc in found[:5]:
            kb = media_result_buttons(str(doc['_id']), doc.get('title',''))
            try:
                if doc.get('poster_file_id'):
                    await client.send_photo(chat_id=message.chat.id, photo=doc['poster_file_id'], caption=doc.get('title'), reply_markup=kb)
                else:
                    await client.send_message(chat_id=message.chat.id, text=doc.get('title'), reply_markup=kb)
            except Exception as e:
                await message.reply(doc.get('title'))

