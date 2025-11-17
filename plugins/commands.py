# command.py
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from Script import *
from config import * # Import start image from config
import asyncio

def register_commands(app: Client):
    @app.on_message(filters.private & filters.command(["start"]))
    async def start(client, message):
        user_id = message.chat.id
        old = insert(int(user_id))  # Make sure `insert` is defined elsewhere

        try:
            id = message.text.split(' ')[1]
        except IndexError:
            id = None

        # Send loading sticker
        loading_sticker_message = await message.reply_sticker(
            "CAACAgUAAxkBAAJZtmZSPxpeDEIwobQtSQnkeGbwNjsyAAJjDgACjPuwVS9WyYuOlsqENQQ"
        )
        await asyncio.sleep(2)
        await loading_sticker_message.delete()

        # Start text
        text = f"""Hello {message.from_user.mention} \n\n➻ This Is An Advanced And Yet Powerful Rename Bot.\n\n➻ Using This Bot You Can Rename And Change Thumbnail Of Your Files.\n\n➻ You Can Also Convert Video To File Aɴᴅ File To Video.\n\n➻ This Bot Also Supports Custom Thumbnail And Custom Caption.\n\n<b>Bot Is Made By @AgsModsOG</b>"""

        # Inline buttons
        button = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("📢 Updates", url="https://t.me/AgsModsOG"),
                InlineKeyboardButton("💬 Support", url="https://t.me/AgsModsOG")
            ],
            [
                InlineKeyboardButton("🛠️ Help", callback_data='help'),
                InlineKeyboardButton("❤️‍🩹 About", callback_data='about')
            ],
            [
                InlineKeyboardButton("🧑‍💻 Developer 🧑‍💻", url="https://t.me/ags_mods_bot")
            ]
        ])

        # Send start photo with caption and buttons
        await message.reply_photo(
            photo=START_PIC,
            caption=text,
            reply_markup=button,
            quote=True
        )
