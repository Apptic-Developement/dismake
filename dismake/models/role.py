from __future__ import annotations

from typing import TYPE_CHECKING, Any


from enum import IntFlag
from ..utils import get_as_snowflake
from .permissions import Permissions


if TYPE_CHECKING:
    from dismake.types import Role as RolePayload, RoleTag as RoleTagPayload
    from typing import Optional


__all__ = ("Role",)


class RoleFlags(IntFlag):
    IN_PROMPT = 1 << 0


class RoleTag:
    def __init__(self, payload: RoleTagPayload) -> None:
        self.bot_id: Optional[int] = get_as_snowflake(payload, "bot_id")
        self.integration_id: Optional[int] = get_as_snowflake(payload, "integration_id")
        self.subscription_listing_id: Optional[int] = get_as_snowflake(
            payload, "subscription_listing_id"
        )
        self.premium_subscriber: bool = payload.get("premium_subscriber", False) is None
        self.available_for_purchase: bool = (
            payload.get("available_for_purchase", False) is None
        )
        self.guild_connections: bool = payload.get("guild_connections", False) is None


class PartialRole:
    def __init__(self, app: Any, id: int):
        self._app = app
        self.id: int = id


class Role(PartialRole):
    def __init__(self, app: Any, payload: RolePayload):
        super().__init__(app=app, id=int(payload["id"]))
        self._payload = payload
        self.name: str = payload["name"]
        self.color = None  # TODO
        self.hoist: bool = payload["hoist"]
        self.icon: Optional[str] = payload.get("icon")
        self.unicode_emoji: Optional[str] = payload.get("unicode_emoji")
        self.position: int = payload["position"]
        self.managed: int = payload["position"]
        self.mentionable: bool = payload["mentionable"]
        self.flags: RoleFlags = RoleFlags(payload["flags"])

    @property
    def tags(self) -> RoleTag | None:
        if payload := self._payload.get("tags"):
            return RoleTag(payload)
        else:
            return None

    @property
    def permissions(self) -> Permissions | None:
        if perms := self._payload.get("permissions"):
            try:
                value = int(perms)
            except ValueError:
                return None
            else:
                return Permissions(value)
        else:
            return None
