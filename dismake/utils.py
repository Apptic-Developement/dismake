from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Optional, Sequence, overload

from colorlog import ColoredFormatter, StreamHandler

__all__: Sequence[str] = ("get_as_snowflake", "setup_logging", "parse_time", "snowflake_time")


DISCORD_EPOCH = 1420070400000

def get_as_snowflake(data: Any, key: str) -> Optional[int]:
    try:
        value = data[key]
    except KeyError:
        return None
    else:
        return value and int(value)


def _get_color_formatter(
    show_time: bool = True,
    show_name: bool = True,
    show_level: bool = True,
    show_message: bool = True,
) -> ColoredFormatter:
    message = ""
    if show_time:
        message += "%(time_log_color)s%(asctime)s%(reset)-5s"

    if show_name:
        message += "%(base_log_color)s%(name)s%(reset)-5s"

    if show_level:
        message += "%(log_color)s%(levelname)s%(reset)-5s"

    if show_message:
        message += "%(message_log_color)s%(message)s%(reset)-5s"
    return ColoredFormatter(
        message,
        log_colors={
            "DEBUG": "cyan",
            "INFO": "blue",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red,bg_white",
        },
        secondary_log_colors={
            "message": {
                "DEBUG": "white",
                "INFO": "white",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_red",
            },
            "time": {
                "DEBUG": "bold_white",
                "INFO": "bold_white",
                "WARNING": "bold_white",
                "ERROR": "bold_white",
                "CRITICAL": "bold_white",
            },
            "base": {
                "DEBUG": "bold_blue",
                "INFO": "bold_blue",
                "WARNING": "bold_blue",
                "ERROR": "bold_blue",
                "CRITICAL": "bold_blue",
            },
        },
        datefmt="%Y-%m-%d %H:%M:%S %p",
    )


def setup_logging(level: int = logging.INFO) -> None:
    logger = logging.getLogger()
    logger.setLevel(level)
    handler = StreamHandler()
    handler.setFormatter(_get_color_formatter())
    logger.addHandler(handler)


@overload
def parse_time(timestamp: None) -> None:
    ...


@overload
def parse_time(timestamp: Optional[str]) -> Optional[datetime]:
    ...


def parse_time(timestamp: Optional[str]) -> Optional[datetime]:
    if timestamp:
        datetime.fromisoformat(timestamp)

    return None


def snowflake_time(id: int, /) -> datetime:
    """Returns the creation time of the given snowflake.


    Parameters
    -----------
    id: int
        The snowflake ID.

    Returns
    --------
    datetime
        An aware datetime in UTC representing the creation time of the snowflake.
    """
    timestamp = ((id >> 22) + DISCORD_EPOCH) / 1000
    return datetime.fromtimestamp(timestamp, tz=timezone.utc)