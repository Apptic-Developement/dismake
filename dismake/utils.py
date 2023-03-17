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
from rich.logging import RichHandler
handler = RichHandler()