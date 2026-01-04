import asyncio
import logging
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

from app.bots.player.router import player_router
from app.config.logging import setup_logging
from app.config.settings import load_settings
from app.container import init_container, shutdown_container, get_access_service


async def main():
    # Always load .env from services/access-service/.env (stable)
    load_dotenv()

    setup_logging()
    settings = load_settings()

    logger = logging.getLogger("gatecraft")
    if not settings.player_bot_token:
        raise RuntimeError("PLAYER_BOT_TOKEN is not set")

    await init_container(settings)

    bot = Bot(
        token=settings.player_bot_token,
        default=DefaultBotProperties(parse_mode="HTML"),
    )

    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(player_router)

    # ✅ DI: put service into dispatcher context
    dp["access_service"] = get_access_service()

    logger.info("Starting GateCraft PlayerBot polling...")
    try:
        await dp.start_polling(bot)
    finally:
        await shutdown_container()


if __name__ == "__main__":
    asyncio.run(main())
