import asyncio
import logging

from app.adapters.rcon.client import RCONClient, RCONError

logger = logging.getLogger("gatecraft.rcon")


class RCONService:
    def __init__(self, host: str, port: int, password: str, timeout: int = 3):
        self.host = host
        self.port = port
        self.password = password
        self.timeout = timeout

    async def run(self, command: str, retries: int = 2) -> str:
        last_exc: Exception | None = None
        for attempt in range(retries + 1):
            try:
                client = RCONClient(self.host, self.port, self.password, self.timeout)
                await client.connect()
                resp = await client.command(command)
                await client.close()
                return resp
            except Exception as e:
                last_exc = e
                logger.warning("RCON command failed attempt=%s cmd=%s err=%s", attempt, command, e)
                await asyncio.sleep(0.3)

        raise last_exc or RCONError("Unknown RCON error")

    async def whitelist_add(self, nickname: str) -> str:
        return await self.run(f"whitelist add {nickname}")

    async def whitelist_remove(self, nickname: str) -> str:
        return await self.run(f"whitelist remove {nickname}")

    async def whitelist_list(self) -> str:
        return await self.run("whitelist list")

    async def list_online(self) -> str:
        return await self.run("list")
