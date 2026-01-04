import asyncio
import logging
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv

from app.bots.admin.router import admin_router
from app.config.logging import setup_logging
from app.config.settings import load_settings
from app.container import init_container, shutdown_container, get_access_service, get_notifier


async def main():
    load_dotenv()

    setup_logging()
    settings = load_settings()

    logger = logging.getLogger("gatecraft")
    if not settings.admin_bot_token:
        raise RuntimeError("ADMIN_BOT_TOKEN is not set")

    await init_container(settings)

    bot = Bot(
        token=settings.admin_bot_token,
        default=DefaultBotProperties(parse_mode="HTML"),
    )

    dp = Dispatcher()
    dp.include_router(admin_router)

    # ✅ DI
    dp["access_service"] = get_access_service()
    dp["notifier"] = get_notifier()
    dp["settings"] = settings

    logger.info("Starting GateCraft AdminBot polling...")
    try:
        await dp.start_polling(bot)
    finally:
        await shutdown_container()


if __name__ == "__main__":
    asyncio.run(main())
