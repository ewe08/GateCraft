import aiomysql

from app.adapters.storage.mysql_repo import MySQLRepo
from app.domain.access_service import AccessService
from app.config.settings import Settings
from app.adapters.telegram.notifier import Notifier

pool: aiomysql.Pool | None = None
repo: MySQLRepo | None = None
access_service: AccessService | None = None
notifier: Notifier | None = None


async def init_container(settings: Settings):
    global pool, repo, access_service, notifier

    pool = await aiomysql.create_pool(
        host=settings.mysql_host,
        port=settings.mysql_port,
        user=settings.mysql_user,
        password=settings.mysql_password,
        db=settings.mysql_db,
        autocommit=True,
        minsize=1,
        maxsize=10,
    )

    repo = MySQLRepo(pool)
    access_service = AccessService(repo)
    notifier = Notifier(settings.player_bot_token)


async def shutdown_container():
    global pool
    if pool:
        pool.close()
        await pool.wait_closed()


def get_access_service() -> AccessService:
    if access_service is None:
        raise RuntimeError("AccessService is not initialized")
    return access_service


def get_notifier() -> Notifier:
    if notifier is None:
        raise RuntimeError("Notifier is not initialized")
    return notifier


def get_pool() -> aiomysql.Pool:
    if pool is None:
        raise RuntimeError("MySQL pool is not initialized")
    return pool
