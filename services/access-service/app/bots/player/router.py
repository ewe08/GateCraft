from aiogram import Router

from .handlers import start, register, status, online, dbdebug
from .middlewares.rate_limit import RateLimitMiddleware


def setup_player_router() -> Router:
    router = Router(name="player_router")

    router.message.middleware(RateLimitMiddleware())
    router.callback_query.middleware(RateLimitMiddleware())

    router.include_router(start.router)
    router.include_router(register.router)
    router.include_router(status.router)
    router.include_router(online.router)
    router.include_router(dbdebug.router)


    return router


player_router = setup_player_router()

__all__ = ("player_router",)
