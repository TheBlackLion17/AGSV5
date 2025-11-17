from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# -----------------------------------------------------------
# SEASONS KEYBOARD
# -----------------------------------------------------------
def seasons_keyboard(series_doc):
    """
    Create season selection buttons.
    series_doc must contain:
    {
        '_id': ObjectId,
        'seasons': [
            {'season_no': 1, 'quality': {...}},
            {'season_no': 2, 'quality': {...}},
            ...
        ]
    }
    """

    buttons = []

    for season in series_doc.get("seasons", []):
        buttons.append([
            InlineKeyboardButton(
                f"Season {season['season_no']}",
                callback_data=f"season_{series_doc['_id']}_{season['season_no']}"
            )
        ])

    # Back Button
    buttons.append([
        InlineKeyboardButton("⬅ Back", callback_data="back_menu")
    ])

    return InlineKeyboardMarkup(buttons)


# -----------------------------------------------------------
# QUALITY KEYBOARD
# -----------------------------------------------------------
def quality_keyboard(series_id, season_no, qualities_dict):
    """
    qualities_dict example:
    {
        "720p": [...],
        "1080p": [...],
        "HDRip": [...],
    }
    """

    buttons = []

    for quality in qualities_dict.keys():
        safe_q = quality.replace(" ", "_")
        buttons.append([
            InlineKeyboardButton(
                quality,
                callback_data=f"quality_{series_id}_{season_no}_{safe_q}"
            )
        ])

    buttons.append([
        InlineKeyboardButton("⬅ Back", callback_data="back_menu")
    ])

    return InlineKeyboardMarkup(buttons)


# -----------------------------------------------------------
# LANGUAGES KEYBOARD
# -----------------------------------------------------------
def languages_keyboard(series_id, languages):
    """
    languages example:
    ["English", "Hindi", "Tamil", "Telugu"]
    """

    buttons = []

    for lang in languages:
        buttons.append([
            InlineKeyboardButton(
                lang,
                callback_data=f"lang_{series_id}_{lang}"
            )
        ])

    buttons.append([
        InlineKeyboardButton("⬅ Back", callback_data="back_menu")
    ])

    return InlineKeyboardMarkup(buttons)
