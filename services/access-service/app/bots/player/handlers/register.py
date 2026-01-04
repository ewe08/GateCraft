import logging
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from app.domain.access_service import AccessService
from app.utils.validators import is_valid_nickname
from ..ui.messages import (
    ASK_NICKNAME_TEXT,
    INVALID_NICK_TEXT,
    REGISTER_SENT_TEXT,
    SERVICE_UNAVAILABLE_TEXT,
)

router = Router(name="player_register")
logger = logging.getLogger("gatecraft.player")


class RegisterFlow(StatesGroup):
    waiting_nickname = State()


@router.message(Command("register"))
async def cmd_register(message: Message, state: FSMContext, access_service: AccessService):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await state.set_state(RegisterFlow.waiting_nickname)
        return await message.answer(ASK_NICKNAME_TEXT)

    nickname = parts[1].strip()
    await handle_registration(message, nickname, access_service)
    await state.clear()


@router.callback_query(F.data == "player:register")
async def cb_register(callback: CallbackQuery, state: FSMContext):
    await state.set_state(RegisterFlow.waiting_nickname)
    await callback.message.answer(ASK_NICKNAME_TEXT)
    await callback.answer()


@router.message(RegisterFlow.waiting_nickname)
async def fsm_receive_nickname(message: Message, state: FSMContext, access_service: AccessService):
    nickname = message.text.strip()
    await handle_registration(message, nickname, access_service)
    await state.clear()


async def handle_registration(message: Message, nickname: str, access_service: AccessService):
    user_id = message.from_user.id
    logger.debug("Handling registration for user_id=%s with nickname=%s", user_id, nickname)
    
    if not is_valid_nickname(nickname):
        logger.warning("User %s provided invalid nickname=%s", user_id, nickname)
        return await message.answer(INVALID_NICK_TEXT)

    try:
        logger.debug("Submitting registration request for user_id=%s nickname=%s", user_id, nickname)
        await access_service.register(user_id, nickname)
    except Exception as e:
        logger.exception("Registration failed for user_id=%s nickname=%s: %s", user_id, nickname, e)
        return await message.answer(SERVICE_UNAVAILABLE_TEXT)

    logger.info("User %s successfully registered with nickname=%s", user_id, nickname)
    return await message.answer(REGISTER_SENT_TEXT)
