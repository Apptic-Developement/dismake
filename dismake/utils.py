from __future__ import annotations

import logging
from rich.logging import RichHandler
from typing import Iterable

__all__ = ("chunk", "init_logging")

format = f"%(name)s - %(levelname)s %(message)s"

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": True,
    "handlers": {
        "console": {
            "class": "rich.logging.RichHandler",
            "formatter": "default",
            "show_time": False,
            "rich_tracebacks": True,
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

def init_logging(log: logging.Logger):
    log.setLevel(logging.DEBUG)

    handler = RichHandler(show_time=False)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(format)
    handler.setFormatter(formatter)
    log.addHandler(handler)
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
