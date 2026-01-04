from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.domain.access_service import AccessService
from app.adapters.telegram.notifier import Notifier
from app.config.settings import Settings

router = Router(name="admin_approve")


def is_admin(settings: Settings, user_id: int) -> bool:
    return user_id in settings.admin_ids


@router.callback_query(F.data.startswith("admin:approve:"))
async def cb_approve(
    callback: CallbackQuery,
    access_service: AccessService,
    notifier: Notifier,
    settings: Settings,
):
    if not is_admin(settings, callback.from_user.id):
        await callback.answer("Access denied", show_alert=True)
        return

    request_id = int(callback.data.split(":")[-1])
    req = await access_service.approve(request_id)
    if not req:
        await callback.message.answer("⚠️ Request not found or already processed.")
        await callback.answer()
        return

    await notifier.notify_player(
        req["tg_user_id"],
        f"✅ Approved! You are now whitelisted as <code>{req['nickname']}</code>."
    )

    await callback.message.answer(f"✅ Approved: <code>{req['nickname']}</code>")
    await callback.answer()


@router.callback_query(F.data.startswith("admin:reject:"))
async def cb_reject(
    callback: CallbackQuery,
    access_service: AccessService,
    notifier: Notifier,
    settings: Settings,
):
    if not is_admin(settings, callback.from_user.id):
        await callback.answer("Access denied", show_alert=True)
        return

    request_id = int(callback.data.split(":")[-1])
    req = await access_service.reject(request_id)
    if not req:
        await callback.message.answer("⚠️ Request not found or already processed.")
        await callback.answer()
        return

    await notifier.notify_player(
        req["tg_user_id"],
        f"❌ Rejected. Your request for <code>{req['nickname']}</code> was rejected."
    )

    await callback.message.answer(f"❌ Rejected: <code>{req['nickname']}</code>")
    await callback.answer()
