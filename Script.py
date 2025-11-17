

class script(object):

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

    RESTART_GC_TXT = """
<b>🔄 𝖡𝗈𝗍 𝖱𝖾𝗌𝗍𝖺𝗋𝗍𝖾𝖽!</b>

📅 𝖣𝖺𝗍𝖾 : <code>{}</code>  
⏰ 𝖳𝗂𝗆𝖾 : <code>{}</code>  
🌐 𝖳𝗂𝗆𝖾𝗓𝗈𝗇𝖾 : <code>Asia/Kolkata</code>  
🛠️ 𝖡𝗎𝗂𝗅𝖽 𝖲𝗍𝖺𝗍𝗎𝗌 : <code>𝗏2 """

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
    LOG_MSG = "📥 User: {user} | Action: {action} | Details: {details}"
