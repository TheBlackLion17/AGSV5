from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def make_season_buttons(series_id, seasons):
    buttons = []
    for s in seasons:
        buttons.append([InlineKeyboardButton(f"Season {s['season_no']}", callback_data=f"season_{series_id}_{s['season_no']}")])
    buttons.append([InlineKeyboardButton("Back", callback_data="back_menu")])
    return InlineKeyboardMarkup(buttons)

def make_quality_buttons(series_id, season_no, qualities):
    buttons = []
    for q in qualities:
        buttons.append([InlineKeyboardButton(q, callback_data=f"quality_{series_id}_{season_no}_{q}")])
    buttons.append([InlineKeyboardButton("Back", callback_data="back_menu")])
    return InlineKeyboardMarkup(buttons)
