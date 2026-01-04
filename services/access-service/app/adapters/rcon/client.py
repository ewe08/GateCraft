import asyncio
import struct


class RCONError(Exception):
    pass


class RCONClient:
    """
    Minimal async RCON client for Minecraft (Source RCON protocol).
    """

    def __init__(self, host: str, port: int, password: str, timeout: int = 3):
        self.host = host
        self.port = port
        self.password = password
        self.timeout = timeout
        self._reader: asyncio.StreamReader | None = None
        self._writer: asyncio.StreamWriter | None = None
        self._req_id = 0

    async def connect(self):
        self._reader, self._writer = await asyncio.wait_for(
            asyncio.open_connection(self.host, self.port),
            timeout=self.timeout,
        )
        await self._auth()

    async def close(self):
        if self._writer:
            self._writer.close()
            try:
                await self._writer.wait_closed()
            except Exception:
                pass

    async def command(self, cmd: str) -> str:
        resp_id, resp_type, payload = await self._send_packet(2, cmd)  # 2 = exec
        if resp_id == -1:
            raise RCONError("RCON command failed (bad auth or server error)")
        return payload

    async def _auth(self):
        resp_id, _, _ = await self._send_packet(3, self.password)  # 3 = auth
        if resp_id == -1:
            raise RCONError("RCON authentication failed")

    async def _send_packet(self, ptype: int, payload: str):
        if not self._writer or not self._reader:
            raise RCONError("Not connected")

        self._req_id += 1
        req_id = self._req_id

        data = payload.encode("utf-8") + b"\x00"
        packet = struct.pack("<ii", req_id, ptype) + data + b"\x00"
        length = struct.pack("<i", len(packet))

        self._writer.write(length + packet)
        await self._writer.drain()

        raw_len = await asyncio.wait_for(self._reader.readexactly(4), timeout=self.timeout)
        (resp_len,) = struct.unpack("<i", raw_len)
        resp_data = await asyncio.wait_for(self._reader.readexactly(resp_len), timeout=self.timeout)

        resp_id, resp_type = struct.unpack("<ii", resp_data[:8])
        resp_payload = resp_data[8:-2].decode("utf-8", errors="ignore")

        return resp_id, resp_type, resp_payload
