from __future__ import annotations

from typing import TYPE_CHECKING, Any

from fastapi import Request

if TYPE_CHECKING:
    ...

__all__ = ("User",)


class User:
    def __init__(self, request: Request, data: dict[Any, Any]):
        self._request = request
        self._data = data
