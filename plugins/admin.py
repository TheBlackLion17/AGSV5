from pyrogram import filters
from config import ADMINS, DUMP_CHANNELS
from database.mongodb import settings_col, media_col

async def register_admin(app):
    @app.on_message(filters.command('set_dump') & filters.user(ADMINS))
    async def set_dump(client, message):
        # usage: /set_dump @channelusername
        if len(message.command) < 2:
            return await message.reply('Usage: /set_dump @channelusername')
        ch = message.command[1]
        await settings_col.update_one({'_id':'main'}, {'$set': {'dump_channels': ch}}, upsert=True)
        await message.reply(f'Set dump channel to {ch}')

    @app.on_message(filters.command('index_channel') & filters.user(ADMINS))
    async def index_channel(client, message):
        # usage: reply to a channel message with /index_channel to index that single message
        if not message.reply_to_message:
            return await message.reply('Reply to a message in the dump channel to index it')
        msg = message.reply_to_message
        await media_col.update_one({'chat_id': msg.chat.id, 'message_id': msg.message_id}, {'$set': {
            'chat_id': msg.chat.id,
            'message_id': msg.message_id,
            'file_id': (msg.document or msg.video or msg.animation).file_id,
            'title': msg.caption or (msg.document.file_name if msg.document else 'untitled')
        }}, upsert=True)
        await message.reply('Indexed message')

    @app.on_message(filters.command('stats') & filters.user(ADMINS))
    async def stats(client, message):
        total = await media_col.count_documents({})
        users = await settings_col.count_documents({'_id':{'$exists':True}})
        await message.reply(f'Media count: {total}')


---
