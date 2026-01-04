from aiogram import Router

from .handlers import start, pending, approve, reject, whitelist


def setup_admin_router() -> Router:
    router = Router(name="admin_router")
    router.include_router(start.router)
    router.include_router(pending.router)
    router.include_router(approve.router)
    router.include_router(reject.router)
    router.include_router(whitelist.router)
    return router


admin_router = setup_admin_router()

__all__ = ("admin_router",)
