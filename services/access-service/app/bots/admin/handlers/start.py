from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from app.config.settings import load_settings

router = Router(name="admin_start")


def is_admin(user_id: int) -> bool:
    settings = load_settings()
    return user_id in settings.admin_ids


@router.message(CommandStart())
async def cmd_start(message: Message):
    if not is_admin(message.from_user.id):
        return await message.answer("⛔ Access denied.")
    await message.answer("🛠️ GateCraft Admin Panel is ready.\nUse /pending to see requests.")


@router.message(Command("help"))
async def cmd_help(message: Message):
    if not is_admin(message.from_user.id):
        return await message.answer("⛔ Access denied.")
    await message.answer("Commands:\n• <code>/pending</code> — list pending requests")
