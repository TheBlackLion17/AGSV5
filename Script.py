class script:
# script.py
# Contains long texts, captions, button labels, messages, etc.

class script:

    START_TXT = """
👋 **Hello {mention}!**

I'm your assistant bot.  
Send me the name of any **movie or series** and I'll fetch it for you.

Use /help for more information.
"""

    HELP_TXT = """
📘 **Help Menu**

Here’s what I can do:

🔍 **Auto Search**
• Just send the name of any series/movie.
• Bot will search and give results.

📥 **Auto Index**
• Automatically indexes new files in configured channels.

🛠 **Admin Commands**
• /stats - View bot stats  
• /broadcast <text> - Send message to all users  
• /addseries <JSON> - Insert/Update series manually  

If you need custom features, contact the admin.
"""

    ABOUT_TXT = """
🤖 **About This Bot**

• Language: Python  
• Library: Pyrogram  
• Database: MongoDB  
• Features: AutoFilter, AutoIndex, File Cache, User Logs

Developer: **@yourusername**
"""

    # When no result found
    NO_RESULT = """
❌ **No results found!**
Try searching with a different name.
"""

    # When an internal error occurs
    ERROR_MSG = """
⚠️ Something went wrong.
Please try again later.
"""

    # Buttons
    BUTTONS = {
        "help": "🆘 Help",
        "about": "ℹ️ About",
        "close": "❌ Close",
        "back": "🔙 Back"
    }

    # For sending series info
    SERIES_TEMPLATE = """
🎬 **{title}**

📁 Total Seasons: {season_count}
📦 Quality: {quality}

Use the buttons below to view files.
"""

    # Logging messages
    LOG_MESSAGE = "📥 User: {user} | Action: {action} | Details: {details}"
