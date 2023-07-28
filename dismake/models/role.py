from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import Request
from ..utils import get_as_snowflake
from ..types import Undefined


if TYPE_CHECKING:
    from ..types import Role as RolePayload, RoleTag as RoleTagPayload, UndefinedType
    from typing import Optional


__all__ = ("Role",)


class RoleTag:
    def __init__(self, payload: RoleTagPayload) -> None:
        self.bot_id: Optional[int] = get_as_snowflake(payload, 'bot_id')
        self.integration_id: Optional[int] = get_as_snowflake(payload, 'integration_id')
        self.subscription_listing_id: Optional[int] = get_as_snowflake(payload, 'subscription_listing_id')
        self.premium_subscriber: bool = payload.get('premium_subscriber', UndefinedType) is None
        self.available_for_purchase: bool = payload.get('available_for_purchase', Undefined) is None
        self.guild_connections: bool = payload.get('guild_connections', Undefined) is None
        ...

class Role:
    def __init__(self, request: Request, payload: RolePayload):
        self._request = request
        self._payload = payload
        self.id: int = int(payload["id"])
        self.name: str = payload["name"]
        # self.color: 
        self.hoist: bool = payload["hoist"]
        self.icon: Optional[str] = payload.get('icon')
        self.unicode_emoji: Optional[str] = payload.get('unicode_emoji')
        self.position: int = payload["position"]
        # self.permissions: 
        self.managed: int = payload["position"]
        self.mentionable: bool = payload["mentionable"]
        # self.flags: 

    @property
    def tags(self) -> RoleTag | None:
        if  (payload := self._payload.get('tags')):
            return RoleTag(payload)
        else:
            return None