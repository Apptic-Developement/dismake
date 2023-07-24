from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import Request

if TYPE_CHECKING:
    ...

__all__ = (
    "Member",
)

class Member:
    def __init__(self, request: Request, data):
        self._request = request
        self._data = data