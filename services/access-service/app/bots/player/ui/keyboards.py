from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📝 Register", callback_data="player:register"),
                InlineKeyboardButton(text="📌 My status", callback_data="player:status"),
            ],
            [
                InlineKeyboardButton(text="🟢 Online", callback_data="player:online"),
            ],
        ]
    )
