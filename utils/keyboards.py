from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def start_keyboard():
    kb = [
        [InlineKeyboardButton('🔎 Search', switch_inline_query_current_chat='')],
        [InlineKeyboardButton('📡 Browse dumps', callback_data='browse_dumps')]
    ]
    return InlineKeyboardMarkup(kb)


def media_result_buttons(media_id: str, title: str):
    kb = [
        [InlineKeyboardButton('📺 View Series', callback_data=f'series_{media_id}')],
        [InlineKeyboardButton('▶️ Send', callback_data=f'send_{media_id}')]
    ]
    return InlineKeyboardMarkup(kb)


def series_navigation_buttons(series_name: str, season: int):
    # list qualities or episodes
    kb = [
        [InlineKeyboardButton('Choose Quality', callback_data=f'qualities|{series_name}|{season}')],
        [InlineKeyboardButton('Back', callback_data='back_to_search')]
    ]
    return InlineKeyboardMarkup(kb)


def make_paginated_buttons(items, prefix, page=0, per_page=8):
    kb = []
    start = page * per_page
    for i, item in enumerate(items[start:start+per_page]):
        kb.append([InlineKeyboardButton(item['label'], callback_data=f"{prefix}|{item['id']}")])
    nav = []
    if start > 0:
        nav.append(InlineKeyboardButton('⬅️ Prev', callback_data=f'{prefix}|page|{page-1}'))
    if start + per_page < len(items):
        nav.append(InlineKeyboardButton('Next ➡️', callback_data=f'{prefix}|page|{page+1}'))
    if nav:
        kb.append(nav)
    return InlineKeyboardMarkup(kb)
