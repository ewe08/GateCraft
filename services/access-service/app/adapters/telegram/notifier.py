import logging

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties

logger = logging.getLogger("gatecraft.notify")


class Notifier:
    def __init__(self, player_bot_token: str):
        self.player_bot = Bot(
            token=player_bot_token,
            default=DefaultBotProperties(parse_mode="HTML"),
        )

    async def notify_player(self, tg_user_id: int, text: str):
        try:
            await self.player_bot.send_message(tg_user_id, text)
        except Exception as e:
            logger.exception("Failed to notify player tg_id=%s: %s", tg_user_id, e)
