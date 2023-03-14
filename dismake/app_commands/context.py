from __future__ import annotations
from typing import Any

from fastapi import Request


__all__ = ("CommandContext",)


class CommandContext:
    def __init__(self, request: Request, **data: dict[str, Any]) -> None:
        ...
