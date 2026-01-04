import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    # Telegram
    player_bot_token: str
    admin_bot_token: str
    admin_ids: list[int]

    # MySQL
    mysql_host: str
    mysql_port: int
    mysql_user: str
    mysql_password: str
    mysql_db: str

    # RCON
    rcon_host: str
    rcon_port: int
    rcon_password: str
    rcon_timeout: int

    # Misc
    log_level: str = "INFO"


def _parse_admin_ids(raw: str) -> list[int]:
    raw = (raw or "").strip()
    if not raw:
        return []
    parts = [p.strip() for p in raw.split(",") if p.strip()]
    return [int(p) for p in parts]


def load_settings() -> Settings:
    return Settings(
        player_bot_token=os.getenv("PLAYER_BOT_TOKEN", "").strip(),
        admin_bot_token=os.getenv("ADMIN_BOT_TOKEN", "").strip(),
        admin_ids=_parse_admin_ids(os.getenv("ADMIN_IDS", "")),

        mysql_host=os.getenv("MYSQL_HOST", "mysql"),
        mysql_port=int(os.getenv("MYSQL_PORT", "3306")),
        mysql_user=os.getenv("MYSQL_USER", "gatecraft"),
        mysql_password=os.getenv("MYSQL_PASSWORD", ""),
        mysql_db=os.getenv("MYSQL_DATABASE", "gatecraft"),

        rcon_host=os.getenv("RCON_HOST", "mc-server"),
        rcon_port=int(os.getenv("RCON_PORT", "25575")),
        rcon_password=os.getenv("RCON_PASSWORD", ""),
        rcon_timeout=int(os.getenv("RCON_TIMEOUT", "3")),

        log_level=os.getenv("LOG_LEVEL", "INFO"),
    )
