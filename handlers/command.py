
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from Script import *
from config import *



def register_commands(app: Client):
    @app.on_message(filters.command("start") & filters.private)
    async def start_command(client, message):
        """Handle /start command with photo, text, and buttons"""

        # Create inline keyboard
        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        script_data.BUTTONS["help"], callback_data="help"
                    ),
                    InlineKeyboardButton(
                        script_data.BUTTONS["about"], callback_data="about"
                    )
                ]
            ]
        )

        # Send photo with caption and buttons
        await client.send_photo(
            chat_id=message.chat.id,
            photo=START_PIC,
            caption=script_data.START_TXT.format(
                mention=message.from_user.mention
            ),
            reply_markup=buttons
        )
