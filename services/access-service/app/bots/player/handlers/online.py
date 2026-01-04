from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.container import access_service
from ..ui.messages import ONLINE_EMPTY_TEXT, ONLINE_FORMAT_TEXT

router = Router(name="player_online")


@router.message(Command("online"))
async def cmd_online(message: Message):
    players = await access_service.get_online()
    if not players:
        return await message.answer(ONLINE_EMPTY_TEXT)

    text = ONLINE_FORMAT_TEXT.format(
        count=len(players),
        players="\n".join(f"• {p}" for p in players),
    )
    await message.answer(text)
