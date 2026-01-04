import logging.config
import os
from pathlib import Path

import yaml


def setup_logging(config_path: str | None = None) -> None:
    if config_path is None:
        config_path = Path(__file__).with_name("logging.yaml")
    else:
        config_path = Path(config_path)

    with config_path.open("r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    env_level = os.getenv("LOG_LEVEL")
    if env_level:
        env_level = env_level.upper()
        config.setdefault("root", {})["level"] = env_level
        config.setdefault("loggers", {}).setdefault("gatecraft", {})["level"] = env_level
        config.setdefault("loggers", {}).setdefault("aiogram", {})["level"] = env_level

    logging.config.dictConfig(config)
