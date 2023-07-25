from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import Request


if TYPE_CHECKING:
    from ..types import User as UserPayload
__all__ = ("User",)


class User:
    def __init__(self, request: Request, payload: UserPayload):
        self._request = request
        # make Final vars
