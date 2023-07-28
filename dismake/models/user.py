from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import Request


if TYPE_CHECKING:
    from ..types import User as UserPayload
    from typing import Optional

    
__all__ = ("User",)


class User:
    def __init__(self, request: Request, payload: UserPayload):
        self._request = request
        self.id: int = int(payload["id"])
        self.username: str = payload["username"]
        self.discriminator: str = payload["discriminator"]
        self.global_name: Optional[str] = payload.get('global_name')
        self.avatar: Optional[str] = payload.get('avatar')
        self.bot: bool = payload["bot"]
        self.system: Optional[bool] = payload.get('system')
        self.mfa_enabled: Optional[bool] = payload.get('mfa_enabled')
        self.banner: Optional[str] = payload.get('banner')
        self.accent_color: Optional[int] = payload.get('accent_color')
        self.locale: Optional[str] = payload.get('locale')
        self.verified: Optional[bool] = payload.get('verified')
        self.email: Optional[str] = payload.get('email')
        # self.flags: 
        # self.premium_type: 
        # self.public_flags: 
        self.avatar_decoration: Optional[str] = payload.get('avatar_decoration')
