import logging
from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from app.config.settings import load_settings

router = Router(name="admin_start")
logger = logging.getLogger("gatecraft.admin")


def is_admin(user_id: int) -> bool:
    settings = load_settings()
    return user_id in settings.admin_ids


@router.message(CommandStart())
async def cmd_start(message: Message):
    user_id = message.from_user.id
    logger.info("Admin /start from user_id=%s", user_id)
    
    if not is_admin(user_id):
        logger.warning("Unauthorized admin /start attempt from user_id=%s", user_id)
        return await message.answer("⛔ Access denied.")
    
    logger.info("Admin panel started for user_id=%s", user_id)
    await message.answer("🛠️ GateCraft Admin Panel is ready.\nUse /pending to see requests.")


@router.message(Command("help"))
async def cmd_help(message: Message):
    user_id = message.from_user.id
    logger.info("Admin /help from user_id=%s", user_id)
    
    if not is_admin(user_id):
        logger.warning("Unauthorized admin /help attempt from user_id=%s", user_id)
        return await message.answer("⛔ Access denied.")
    
    logger.debug("Help command displayed to user_id=%s", user_id)
    await message.answer("Commands:\n• <code>/pending</code> — list pending requests")
