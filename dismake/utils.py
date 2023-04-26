from __future__ import annotations

from typing import Iterable

__all__ = (
    "chunk",
)

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
            "format": "[%(name)s] - %(message)s",
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

def chunk(max_size: int, iterator: Iterable):
    if max_size <= 0:
        raise ValueError('Chunk sizes must be greater than 0.')
    
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