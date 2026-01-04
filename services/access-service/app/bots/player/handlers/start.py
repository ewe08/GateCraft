import logging
from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from ..ui.messages import WELCOME_TEXT
from ..ui.keyboards import main_menu_keyboard

router = Router(name="player_start")
logger = logging.getLogger("gatecraft.player")


@router.message(CommandStart())
async def cmd_start(message: Message):
    user_id = message.from_user.id
    logger.info("User %s initiated /start", user_id)
    logger.debug("Sending welcome menu to user_id=%s", user_id)
    await message.answer(WELCOME_TEXT, reply_markup=main_menu_keyboard())


@router.message(Command("help"))
async def cmd_help(message: Message):
    user_id = message.from_user.id
    logger.info("User %s requested /help", user_id)
    logger.debug("Sending help menu to user_id=%s", user_id)
    await message.answer(WELCOME_TEXT, reply_markup=main_menu_keyboard())
