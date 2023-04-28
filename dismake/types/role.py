from __future__ import annotations

from typing import Any, TypedDict, TYPE_CHECKING

if TYPE_CHECKING:
    from typing_extensions import NotRequired
    from .snowflake import SnowFlake
__all__ = ("RoleTags", "Role")


class RoleTags(TypedDict):
    bot_id: NotRequired[SnowFlake]
    integration_id: NotRequired[SnowFlake]
    premium_subscriber: NotRequired[Any]
    subscription_listing_id: NotRequired[SnowFlake]
    available_for_purchase: NotRequired[Any]
    guild_connections: NotRequired[Any]


class Role(TypedDict):
    id: SnowFlake
    name: str
    color: int
    hoist: bool
    icon: NotRequired[str]
    unicode_emoji: NotRequired[str]
    position: int
    permissions: int
    managed: bool
    mentionable: bool
    tags: NotRequired[RoleTags]
