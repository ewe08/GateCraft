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
    status = await access_service.status(message.from_user.id)
    logger.info("Status request tg_id=%s status=%s", message.from_user.id, status)

    if status == "not_registered":
        return await message.answer(STATUS_NOT_REGISTERED_TEXT)
    if status == "pending":
        return await message.answer(STATUS_PENDING_TEXT)
    if status == "approved":
        return await message.answer(STATUS_APPROVED_TEXT)
    if status == "rejected":
        return await message.answer(STATUS_REJECTED_TEXT)

    return await message.answer("⚠️ Unknown status")
