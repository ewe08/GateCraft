import logging
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.domain.access_service import AccessService
from app.config.settings import Settings
from ..ui.messages import NEW_REQUEST_TEXT, NO_PENDING_TEXT
from ..ui.keyboards import approval_keyboard

router = Router(name="admin_pending")
logger = logging.getLogger("gatecraft.admin")


def is_admin(settings: Settings, user_id: int) -> bool:
    return user_id in settings.admin_ids


@router.message(Command("pending"))
async def cmd_pending(message: Message, access_service: AccessService, settings: Settings):
    user_id = message.from_user.id
    logger.info("Admin pending request from user_id=%s", user_id)
    
    if not is_admin(settings, user_id):
        logger.warning("Unauthorized pending access attempt from user_id=%s", user_id)
        return await message.answer("⛔ Access denied.")

    pending = await access_service.pending()
    logger.debug("Retrieved %d pending requests", len(pending) if pending else 0)
    
    if not pending:
        logger.info("No pending requests found")
        return await message.answer(NO_PENDING_TEXT)

    for req in pending:
        logger.debug("Displaying pending request id=%s nickname=%s", req["id"], req["nickname"])
        await message.answer(
            NEW_REQUEST_TEXT.format(
                nickname=req["nickname"],
                tg_user_id=req["tg_user_id"],
                request_id=req["id"],
            ),
            reply_markup=approval_keyboard(req["id"]),
        )
