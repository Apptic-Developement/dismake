from __future__ import annotations

import inspect
from .types import AsyncFunction

__all__ = (
    "get_args",
)

async def get_args(coro: AsyncFunction):
    signature = inspect.signature(coro)
