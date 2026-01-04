import re

NICKNAME_RE = re.compile(r"^[A-Za-z0-9_]{3,16}$")


def is_valid_nickname(nick: str) -> bool:
    return bool(NICKNAME_RE.match(nick))
