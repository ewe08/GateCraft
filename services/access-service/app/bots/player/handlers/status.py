import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.domain.access_service import AccessService
from ..ui.messages import (
    STATUS_NOT_REGISTERED_TEXT,
    STATUS_PENDING_TEXT,
    STATUS_APPROVED_TEXT,
    STATUS_REJECTED_TEXT,
)

router = Router(name="player_status")
logger = logging.getLogger("gatecraft.player")


@router.message(Command("status"))
async def cmd_status(message: Message, access_service: AccessService):
    user_id = message.from_user.id
    logger.info("User %s requested /status", user_id)
    
    status = await access_service.status(user_id)
    logger.debug("Retrieved status=%s for user_id=%s", status, user_id)

    if status == "not_registered":
        logger.debug("User %s has not_registered status", user_id)
        return await message.answer(STATUS_NOT_REGISTERED_TEXT)
    if status == "pending":
        logger.debug("User %s has pending status", user_id)
        return await message.answer(STATUS_PENDING_TEXT)
    if status == "approved":
        logger.debug("User %s has approved status", user_id)
        return await message.answer(STATUS_APPROVED_TEXT)
    if status == "rejected":
        logger.debug("User %s has rejected status", user_id)
        return await message.answer(STATUS_REJECTED_TEXT)

    logger.warning("User %s has unknown status=%s", user_id, status)
    return await message.answer("⚠️ Unknown status")
