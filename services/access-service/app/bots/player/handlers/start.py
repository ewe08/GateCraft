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
    logger.info("User %s /start", message.from_user.id)
    await message.answer(WELCOME_TEXT, reply_markup=main_menu_keyboard())


@router.message(Command("help"))
async def cmd_help(message: Message):
    logger.info("User %s /help", message.from_user.id)
    await message.answer(WELCOME_TEXT, reply_markup=main_menu_keyboard())
