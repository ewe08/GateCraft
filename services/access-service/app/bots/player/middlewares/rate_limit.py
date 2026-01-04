import time
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


class RateLimitMiddleware(BaseMiddleware):
    def __init__(self, limit_seconds: float = 0.7):
        self.limit_seconds = limit_seconds
        self._last_seen: dict[int, float] = {}

    async def __call__(self, handler, event: TelegramObject, data: dict):
        user = data.get("event_from_user")
        if not user:
            return await handler(event, data)

        now = time.time()
        last = self._last_seen.get(user.id, 0)

        if now - last < self.limit_seconds:
            return  # silently drop

        self._last_seen[user.id] = now
        return await handler(event, data)
    