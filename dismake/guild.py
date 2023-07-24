from __future__ import annotations
from typing import Any

from fastapi import Request

__all__ = (
    "Guild",
)

class Guild:
    def __init__(self, request: Request, data: dict[Any, Any]):
        self._request = request
        self._data = data