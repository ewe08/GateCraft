import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from app.bots.player.router import player_router
from app.bots.admin.router import admin_router
from app.config.logging import setup_logging
from app.config.settings import load_settings
from app.container import init_container, shutdown_container, get_access_service, get_notifier, get_rcon


async def _run_player_bot(token: str):
    logger = logging.getLogger("gatecraft.player")
    bot = Bot(token=token, default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(player_router)

    dp["access_service"] = get_access_service()
    dp["settings"] = load_settings()
    dp["rcon"] = get_rcon()

    logger.info("Run polling for player bot...")
    await dp.start_polling(bot)


async def _run_admin_bot(token: str):
    logger = logging.getLogger("gatecraft.admin")
    bot = Bot(token=token, default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(admin_router)

    dp["access_service"] = get_access_service()
    dp["notifier"] = get_notifier()
    dp["rcon"] = get_rcon()
    dp["settings"] = load_settings()

    logger.info("Run polling for admin bot...")
    await dp.start_polling(bot)


async def main():
    setup_logging()
    settings = load_settings()

    logger = logging.getLogger("gatecraft")
    if not settings.player_bot_token:
        raise RuntimeError("PLAYER_BOT_TOKEN is not set")
    if not settings.admin_bot_token:
        raise RuntimeError("ADMIN_BOT_TOKEN is not set")
    if not settings.admin_ids:
        raise RuntimeError("ADMIN_IDS is not set")

    await init_container(settings)

    logger.info("Starting GateCraft access-service (player + admin bots)...")
    try:
        await asyncio.gather(
            _run_player_bot(settings.player_bot_token),
            _run_admin_bot(settings.admin_bot_token),
        )
    finally:
        await shutdown_container()


if __name__ == "__main__":
    asyncio.run(main())
