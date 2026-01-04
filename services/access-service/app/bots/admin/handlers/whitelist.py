import logging
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.adapters.rcon.service import RCONService

router = Router(name="admin_whitelist")
logger = logging.getLogger("gatecraft.admin")


@router.message(Command("whitelist_add"))
async def cmd_whitelist_add(message: Message, rcon: RCONService):
    user_id = message.from_user.id
    logger.info("User %s requested whitelist_add", user_id)
    
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        logger.warning("User %s sent whitelist_add without nickname", user_id)
        return await message.answer("Usage: /whitelist_add <nickname>")

    nick = parts[1].strip()
    logger.debug("Adding nickname=%s to whitelist by user_id=%s", nick, user_id)
    
    try:
        resp = await rcon.whitelist_add(nick)
        logger.info("Successfully added nickname=%s to whitelist by user_id=%s", nick, user_id)
        await message.answer(f"✅ Whitelist add <code>{nick}</code>\n<pre>{resp}</pre>")
    except Exception as e:
        logger.exception("whitelist_add failed for nickname=%s by user_id=%s", nick, user_id)
        await message.answer(f"❌ RCON error: <code>{e}</code>")


@router.message(Command("whitelist_remove"))
async def cmd_whitelist_remove(message: Message, rcon: RCONService):
    user_id = message.from_user.id
    logger.info("User %s requested whitelist_remove", user_id)
    
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        logger.warning("User %s sent whitelist_remove without nickname", user_id)
        return await message.answer("Usage: /whitelist_remove <nickname>")

    nick = parts[1].strip()
    logger.debug("Removing nickname=%s from whitelist by user_id=%s", nick, user_id)
    
    try:
        resp = await rcon.whitelist_remove(nick)
        logger.info("Successfully removed nickname=%s from whitelist by user_id=%s", nick, user_id)
        await message.answer(f"✅ Whitelist remove <code>{nick}</code>\n<pre>{resp}</pre>")
    except Exception as e:
        logger.exception("whitelist_remove failed for nickname=%s by user_id=%s", nick, user_id)
        await message.answer(f"❌ RCON error: <code>{e}</code>")
