from __future__ import annotations

from fastapi import Request

__all__ = (
    "Member",
)

class Member:
    def __init__(self, request: Request, data: dict):
        self._request = request
        self._data = data