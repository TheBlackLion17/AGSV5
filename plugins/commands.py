# plugins/commands.py
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import START_PIC
from Script import script
import asyncio

@Client.on_message(filters.private & filters.command("start"))
async def start(client, message):
    user_id = message.chat.id
    # Optional: insert user in DB
    # old = insert(int(user_id))

    try:
        id = message.text.split(' ')[1]
    except IndexError:
        id = None

    # Loading sticker
    loading_sticker_message = await message.reply_sticker(
        "CAACAgUAAxkBAAJZtmZSPxpeDEIwobQtSQnkeGbwNjsyAAJjDgACjPuwVS9WyYuOlsqENQQ"
    )
    await asyncio.sleep(2)
    await loading_sticker_message.delete()

    # Start text
    text = script.START_TXT.format(mention=message.from_user.mention)

    # Inline buttons
    button = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🆘 Help", callback_data='help'),
            InlineKeyboardButton("ℹ️ About", callback_data='about')
        ],
        [
            InlineKeyboardButton("📢 Updates", url="https://t.me/AgsModsOG"),
            InlineKeyboardButton("💬 Support", url="https://t.me/AgsModsOG")
        ],
        [
            InlineKeyboardButton("🧑‍💻 Developer", url="https://t.me/ags_mods_bot")
        ]
    ])

    await message.reply_photo(
        photo=START_PIC,
        caption=text,
        reply_markup=button,
        quote=True
    )

# Optional: add callbacks for buttons
@Client.on_callback_query()
async def callbacks(client, query):
    if query.data == "help":
        await query.message.edit_text(
            script.HELP_TXT,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Back", callback_data="start")]
            ])
        )
    elif query.data == "about":
        await query.message.edit_text(
            script.ABOUT_TXT,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Back", callback_data="start")]
            ])
        )
    elif query.data == "start":
        await query.message.edit_text(
            script.START_TXT.format(mention=query.from_user.mention)
        )
