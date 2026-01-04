import logging
from aiogram import Router
from aiogram.types import CallbackQuery

from app.domain.access_service import AccessService
from app.adapters.telegram.notifier import Notifier

router = Router(name="admin_reject")
logger = logging.getLogger("gatecraft.admin")


@router.callback_query(lambda c: c.data and c.data.startswith("admin:reject:"))
async def cb_reject(callback: CallbackQuery,
                    access_service: AccessService,
                    notifier: Notifier):
    admin_id = callback.from_user.id
    request_id = int(callback.data.split(":")[2])
    logger.info("Admin user_id=%s rejecting request_id=%s", admin_id, request_id)

    req = await access_service.reject(request_id)
    if not req:
        logger.warning("Admin user_id=%s tried to reject non-existent request_id=%s", admin_id, request_id)
        return await callback.answer("Request not found or already processed", show_alert=True)

    nickname = req["nickname"]
    tg_user_id = req["tg_user_id"]
    logger.debug("Rejected request_id=%s nickname=%s tg_user_id=%s by admin_id=%s", request_id, nickname, tg_user_id, admin_id)

    # notify player about rejection
    try:
        await notifier.player_rejected(tg_user_id, nickname)
        logger.debug("Player rejection notification sent to tg_user_id=%s for nickname=%s", tg_user_id, nickname)
    except Exception:
        logger.exception("Failed to notify player about rejection tg_id=%s nickname=%s", tg_user_id, nickname)

    # admin feedback
    text = f"❌ Rejected <code>{nickname}</code>\nPlayer has been notified."
    logger.info("Rejection completed for request_id=%s nickname=%s", request_id, nickname)
    await callback.message.answer(text)
    await callback.answer("Rejected ❌")
