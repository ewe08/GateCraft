from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.container import get_pool

router = Router(name="player_dbdebug")


@router.message(Command("dbstatus"))
async def cmd_dbstatus(message: Message):
    tg_id = message.from_user.id
    pool = get_pool()

    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT DATABASE(), @@hostname, @@port")
            db_name, host, port = await cur.fetchone()

            await cur.execute(
                "SELECT tg_user_id, nickname, status FROM users WHERE tg_user_id=%s",
                (tg_id,)
            )
            user_row = await cur.fetchone()

            await cur.execute(
                "SELECT id, nickname, status FROM requests WHERE tg_user_id=%s ORDER BY id DESC LIMIT 5",
                (tg_id,)
            )
            req_rows = await cur.fetchall()

    text = (
        f"DB={db_name} host={host}:{port}\n"
        f"tg_id={tg_id}\n"
        f"users={user_row}\n"
        f"requests={req_rows}\n"
    )

    await message.answer(f"<pre>{text}</pre>")
