from __future__ import annotations

from enum import IntFlag
from typing import TYPE_CHECKING, Sequence, Optional, Tuple

from ..utils import get_as_snowflake
from .permissions import Permissions

if TYPE_CHECKING:
    from dismake import Client
    from dismake.types import Role as RolePayload
    from dismake.types import RoleTag as RoleTagPayload


__all__: Sequence[str] = ("Role",)


class RoleFlags(IntFlag):
    IN_PROMPT = 1 << 0


class RoleTag:
    __slots__: Tuple[str] = ("_payload",)

    def __init__(self, payload: RoleTagPayload) -> None:
        self._payload = payload

    @property
    def bot_id(self) -> Optional[int]:
        return get_as_snowflake(self._payload, "bot_id")

    @property
    def integration_id(self) -> Optional[int]:
        return get_as_snowflake(self._payload, "integration_id")

    @property
    def subscription_listing_id(self) -> Optional[int]:
        return get_as_snowflake(self._payload, "subscription_listing_id")

    @property
    def premium_subscriber(self) -> bool:
        return self._payload.get("premium_subscriber", False) is None

    @property
    def available_for_purchase(self) -> bool:
        return self._payload.get("available_for_purchase", False) is None

    @property
    def guild_connections(self) -> bool:
        return self._payload.get("guild_connections", False) is None


class PartialRole:
    __slots__: Tuple[str, ...] = ("_client", "id")

    def __init__(self, client: Client, id: int):
        self._client = client
        self.id: int = id


class Role(PartialRole):
    __slots__: Tuple[str, ...] = (
        "_payload",
        "name",
        "color",
        "hoist",
        "icon",
        "unicode_emoji",
        "position",
        "managed",
        "mentionable",
        "flags",
    )

    def __init__(self, client: Client, payload: RolePayload):
        super().__init__(client=client, id=int(payload["id"]))
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
    def tags(self) -> Optional[RoleTag]:
        if payload := self._payload.get("tags"):
            return RoleTag(payload)
        else:
            return None

    @property
    def permissions(self) -> Optional[Permissions]:
        if perms := self._payload.get("permissions"):
            try:
                value = int(perms)
            except ValueError:
                return None
            else:
                return Permissions(value)
        else:
            return None