from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.domain.access_service import AccessService
from app.config.settings import Settings
from ..ui.messages import NEW_REQUEST_TEXT, NO_PENDING_TEXT
from ..ui.keyboards import approval_keyboard

router = Router(name="admin_pending")


def is_admin(settings: Settings, user_id: int) -> bool:
    return user_id in settings.admin_ids


@router.message(Command("pending"))
async def cmd_pending(message: Message, access_service: AccessService, settings: Settings):
    if not is_admin(settings, message.from_user.id):
        return await message.answer("⛔ Access denied.")

    pending = await access_service.pending()
    if not pending:
        return await message.answer(NO_PENDING_TEXT)

    for req in pending:
        await message.answer(
            NEW_REQUEST_TEXT.format(
                nickname=req["nickname"],
                tg_user_id=req["tg_user_id"],
                request_id=req["id"],
            ),
            reply_markup=approval_keyboard(req["id"]),
        )
