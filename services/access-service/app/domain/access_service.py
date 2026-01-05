class AccessService:
    def __init__(self, repo):
        self.repo = repo

    async def register(self, tg_user_id: int, nickname: str, tg_username: str | None = None) -> dict:
        return await self.repo.create_request(tg_user_id, nickname, tg_username)

    async def approve(self, request_id: int) -> dict | None:
        return await self.repo.approve_request(request_id)

    async def reject(self, request_id: int) -> dict | None:
        return await self.repo.reject_request(request_id)

    async def pending(self) -> list[dict]:
        return await self.repo.list_pending()

    async def status(self, tg_user_id: int) -> str:
        return await self.repo.get_user_status(tg_user_id)

    async def get_online(self) -> list[str]:
        # TODO: replace with RCON list later
        return ["Steve", "Alex"]
