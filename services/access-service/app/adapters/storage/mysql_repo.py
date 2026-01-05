import aiomysql
from typing import Optional


class MySQLRepo:
    def __init__(self, pool: aiomysql.Pool):
        self.pool = pool

    async def create_request(self, tg_user_id: int, nickname: str, tg_username: str | None = None) -> dict:
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                # 1) Check current user status first
                await cur.execute(
                    "SELECT tg_user_id, tg_username, nickname, status FROM users WHERE tg_user_id=%s",
                    (tg_user_id,),
                )
                user = await cur.fetchone()

                # If already approved, do not downgrade to pending
                if user and user["status"] == "approved":
                    # Optionally update nickname, but keep approved
                    updates = []
                    params = []
                    if user["nickname"] != nickname:
                        updates.append("nickname=%s")
                        params.append(nickname)
                    if tg_username and user.get("tg_username") != tg_username:
                        updates.append("tg_username=%s")
                        params.append(tg_username)
                    if updates:
                        params.append(tg_user_id)
                        await cur.execute(
                            f"UPDATE users SET {', '.join(updates)} WHERE tg_user_id=%s",
                            tuple(params),
                        )
                        await conn.commit()
                    return {
                        "id": None,
                        "tg_user_id": tg_user_id,
                        "nickname": nickname,
                        "tg_username": tg_username,
                        "status": "approved",
                    }

                # 2) If there is already a pending request — return it
                await cur.execute(
                    "SELECT * FROM requests WHERE tg_user_id=%s AND status='pending' ORDER BY id DESC LIMIT 1",
                    (tg_user_id,),
                )
                row = await cur.fetchone()
                if row:
                    return row

                # 3) Create a new pending request
                await cur.execute(
                    "INSERT INTO requests (tg_user_id, tg_username, nickname, status) VALUES (%s, %s, %s, 'pending')",
                    (tg_user_id, tg_username, nickname),
                )
                request_id = cur.lastrowid

                # 4) Upsert user row, but never downgrade approved
                await cur.execute(
                    """
                    INSERT INTO users (tg_user_id, tg_username, nickname, status)
                    VALUES (%s, %s, %s, 'pending') AS new
                    ON DUPLICATE KEY UPDATE
                        tg_username = COALESCE(new.tg_username, users.tg_username),
                        nickname = new.nickname,
                        status = CASE
                            WHEN users.status = 'approved' THEN users.status
                            ELSE 'pending'
                        END
                    """,
                    (tg_user_id, tg_username, nickname),
                )

                await conn.commit()

                await cur.execute("SELECT * FROM requests WHERE id=%s", (request_id,))
                return await cur.fetchone()


    async def approve_request(self, request_id: int) -> Optional[dict]:
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute("SELECT * FROM requests WHERE id=%s", (request_id,))
                req = await cur.fetchone()
                if not req or req["status"] != "pending":
                    return None

                await cur.execute("UPDATE requests SET status='approved' WHERE id=%s", (request_id,))
                await cur.execute(
                    "UPDATE users SET status='approved' WHERE tg_user_id=%s",
                    (req["tg_user_id"],),
                )
                await conn.commit()

                await cur.execute("SELECT * FROM requests WHERE id=%s", (request_id,))
                return await cur.fetchone()

    async def reject_request(self, request_id: int) -> Optional[dict]:
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute("SELECT * FROM requests WHERE id=%s", (request_id,))
                req = await cur.fetchone()
                if not req or req["status"] != "pending":
                    return None

                await cur.execute("UPDATE requests SET status='rejected' WHERE id=%s", (request_id,))
                await cur.execute(
                    "UPDATE users SET status='rejected' WHERE tg_user_id=%s",
                    (req["tg_user_id"],),
                )
                await conn.commit()

                await cur.execute("SELECT * FROM requests WHERE id=%s", (request_id,))
                return await cur.fetchone()

    async def list_pending(self) -> list[dict]:
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(
                    "SELECT * FROM requests WHERE status='pending' ORDER BY created_at ASC LIMIT 50"
                )
                return await cur.fetchall()

    async def get_user_status(self, tg_user_id: int) -> str:
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT status FROM users WHERE tg_user_id=%s", (tg_user_id,))
                row = await cur.fetchone()
                return row[0] if row else "not_registered"
