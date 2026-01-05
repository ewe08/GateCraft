import logging
from aiogram import Router
from aiogram.filters import Command
from aiogram import F
from aiogram.types import Message, CallbackQuery

from app.container import access_service
from app.adapters.rcon.service import RCONService
from ..ui.messages import ONLINE_EMPTY_TEXT, ONLINE_FORMAT_TEXT

router = Router(name="player_online")
logger = logging.getLogger("gatecraft.player")


@router.message(Command("online"))
async def cmd_online(message: Message, rcon: RCONService):
    user_id = message.from_user.id
    logger.info("User %s requested /online", user_id)

    # Try to get online players via RCON
    players = None
    try:
        resp = await rcon.list_online()
        logger.debug("RCON list response: %s", resp)
        # parse typical Minecraft 'list' response: "There are X of a max of Y players online: name1, name2"
        text_part = resp.partition(":")[2].strip()
        if not text_part:
            players = []
        else:
            players = [p.strip() for p in text_part.split(",") if p.strip()]
    except Exception:
        logger.exception("RCON list failed, falling back to access_service")
        try:
            players = await access_service.get_online()
        except Exception:
            logger.exception("Failed to get online players from access_service")
            players = None

    if not players:
        logger.debug("No online players for user_id=%s", user_id)
        return await message.answer(ONLINE_EMPTY_TEXT)

    text = ONLINE_FORMAT_TEXT.format(
        count=len(players),
        players="\n".join(f"• {p}" for p in players),
    )
    logger.debug("Sent online list to user_id=%s with %d players", user_id, len(players))
    await message.answer(text)


@router.callback_query(F.data == "player:online")
async def cb_online(callback: CallbackQuery, rcon: RCONService):
    # reuse the same logic as the message handler by calling it directly
    await cmd_online(callback.message, rcon)
    await callback.answer()
