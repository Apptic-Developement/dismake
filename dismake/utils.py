from __future__ import annotations
import logging

from typing import Iterable

from rich.logging import RichHandler

__all__ = ("chunk",)

format = "%(asctime)s %(name)-15s | %(message)s"

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": True,
    "handlers": {
        "console": {
            "class": "rich.logging.RichHandler",
            "formatter": "default",
            "show_time": False,
            "rich_tracebacks": False,
        },
    },
    "formatters": {
        "default": {
            "format": format,
        },
    },
    "loggers": {
        "uvicorn": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}

def getLogger(name: str, *, level: int = logging.INFO):
    log = logging.getLogger(name)
    handler = RichHandler(show_time=False, rich_tracebacks=True)
    handler.setFormatter(logging.Formatter(format))
    log.addHandler(handler)
    log.setLevel(level)
    return log
def chunk(max_size: int, iterator: Iterable):
    if max_size <= 0:
        raise ValueError("Chunk sizes must be greater than 0.")

    ret = list()
    n = 0
    for i in iterator:
        ret.append(i)
        n += 1
        if n == max_size:
            yield ret
            ret.clear()
            n = 0
    if ret:
        yield ret
