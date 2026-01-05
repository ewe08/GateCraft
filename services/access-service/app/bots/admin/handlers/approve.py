import logging
from aiogram import Router
from aiogram.types import CallbackQuery

from app.domain.access_service import AccessService
from app.adapters.telegram.notifier import Notifier
from app.adapters.rcon.service import RCONService
from app.bots.player.ui.messages import NOTIFY_APPROVED_TEXT

router = Router(name="admin_approve")
logger = logging.getLogger("gatecraft.admin")


@router.callback_query(lambda c: c.data and c.data.startswith("admin:approve:"))
async def cb_approve(callback: CallbackQuery,
                     access_service: AccessService,
                     notifier: Notifier,
                     rcon: RCONService):
    admin_id = callback.from_user.id
    request_id = int(callback.data.split(":")[2])
    logger.info("Admin user_id=%s approving request_id=%s", admin_id, request_id)

    req = await access_service.approve(request_id)
    if not req:
        logger.warning("Admin user_id=%s tried to approve non-existent request_id=%s", admin_id, request_id)
        return await callback.answer("Request not found or already processed", show_alert=True)

    nickname = req["nickname"]
    tg_user_id = req["tg_user_id"]
    logger.debug("Approved request_id=%s nickname=%s tg_user_id=%s by admin_id=%s", request_id, nickname, tg_user_id, admin_id)

    rcon_ok = False
    rcon_error = None
    try:
        await rcon.whitelist_add(nickname)
        rcon_ok = True
        logger.info("RCON whitelist add succeeded for nickname=%s", nickname)
    except Exception as e:
        rcon_error = str(e)
        logger.exception("RCON whitelist add failed nick=%s tg_id=%s", nickname, tg_user_id)

    # notify player
    try:
        await notifier.notify_player(tg_user_id, NOTIFY_APPROVED_TEXT.format(nickname=nickname))
        logger.debug("Player notification sent to tg_user_id=%s for nickname=%s", tg_user_id, nickname)
    except Exception:
        logger.exception("Failed to notify player tg_id=%s nickname=%s", tg_user_id, nickname)

    # admin feedback
    text = f"✅ Approved <code>{nickname}</code>\n"
    if rcon_ok:
        text += "🖥 Whitelist updated via RCON ✅"
    else:
        text += f"⚠️ Approved in DB, but RCON failed: <code>{rcon_error}</code>\n" \
                f"Try /whitelist_add {nickname} later."

    logger.info("Approval completed for request_id=%s nickname=%s rcon_ok=%s", request_id, nickname, rcon_ok)
    await callback.message.answer(text)
    await callback.answer("Approved ✅")
