import logging
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.container import access_service
from ..ui.messages import ONLINE_EMPTY_TEXT, ONLINE_FORMAT_TEXT

router = Router(name="player_online")
logger = logging.getLogger("gatecraft.player")


@router.message(Command("online"))
async def cmd_online(message: Message):
    user_id = message.from_user.id
    logger.info("User %s requested /online", user_id)
    
    players = await access_service.get_online()
    logger.debug("Retrieved %d online players", len(players) if players else 0)
    
    if not players:
        logger.debug("No online players for user_id=%s", user_id)
        return await message.answer(ONLINE_EMPTY_TEXT)

    text = ONLINE_FORMAT_TEXT.format(
        count=len(players),
        players="\n".join(f"• {p}" for p in players),
    )
    logger.debug("Sent online list to user_id=%s with %d players", user_id, len(players))
    await message.answer(text)
