from __future__ import annotations
from fastapi import Request
from ._types import ClientT

__all__ = (
    "CommandContext",
)


class CommandContext:
    def __init__(self, bot: ClientT, request: Request, **kwargs) -> None:
        self.bot = bot
        self.request = request
        