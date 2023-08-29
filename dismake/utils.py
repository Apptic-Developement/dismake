from __future__ import annotations
import typing
import logging
import colorlog

__all__: typing.Sequence[str] = ("get_as_snowflake", "setup_logging")


def get_as_snowflake(data: typing.Any, key: str) -> typing.Optional[int]:
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
) -> colorlog.ColoredFormatter:
    message = ""
    if show_time:
        message += "%(time_log_color)s%(asctime)s%(reset)-5s"

    if show_name:
        message += "%(base_log_color)s%(name)s%(reset)-5s"

    if show_level:
        message += "%(log_color)s%(levelname)s%(reset)-5s"

    if show_message:
        message += "%(message_log_color)s%(message)s%(reset)-5s"
    return colorlog.ColoredFormatter(
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


def setup_logging() -> None:
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    handler = colorlog.StreamHandler()
    handler.setFormatter(_get_color_formatter())
    logger.addHandler(handler)
