import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    player_bot_token: str
    admin_bot_token: str
    admin_ids: set[int]

    mysql_host: str
    mysql_port: int
    mysql_user: str
    mysql_password: str
    mysql_db: str


def load_settings() -> Settings:
    admin_ids = set()
    for x in os.getenv("ADMIN_IDS", "").split(","):
        x = x.strip()
        if x:
            admin_ids.add(int(x))

    return Settings(
        player_bot_token=os.getenv("PLAYER_BOT_TOKEN", ""),
        admin_bot_token=os.getenv("ADMIN_BOT_TOKEN", ""),
        admin_ids=admin_ids,

        mysql_host=os.getenv("MYSQL_HOST", "127.0.0.1"),
        mysql_port=int(os.getenv("MYSQL_PORT", "3306")),
        mysql_user=os.getenv("MYSQL_USER", "gatecraft"),
        mysql_password=os.getenv("MYSQL_PASSWORD", ""),
        mysql_db=os.getenv("MYSQL_DATABASE", "gatecraft"),
    )
