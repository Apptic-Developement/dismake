from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import Request

if TYPE_CHECKING:
    from ..types import Member as MemberPayload

__all__ = ("Member",)


class Member:
    def __init__(self, request: Request, payload: MemberPayload):
        self._request = request
        # make Final vars
