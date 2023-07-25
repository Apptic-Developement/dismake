from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import Request


if TYPE_CHECKING:
    from ..types import Role as RolePayload
__all__ = ("Role",)


class Role:
    def __init__(self, request: Request, payload: RolePayload):
        self._request = request
        # make Final vars
