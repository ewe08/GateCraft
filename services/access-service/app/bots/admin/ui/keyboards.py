from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def approval_keyboard(request_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Approve", callback_data=f"admin:approve:{request_id}"),
                InlineKeyboardButton(text="❌ Reject", callback_data=f"admin:reject:{request_id}"),
            ]
        ]
    )
