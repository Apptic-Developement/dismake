from __future__ import annotations
from typing import TYPE_CHECKING, Optional, TypedDict

if TYPE_CHECKING:
    from .snowflake import Snowflake

__all__ = ("Role", "RoleTag")


class RoleTag(TypedDict):
    bot_id: Optional[Snowflake]
    integration_id: Optional[Snowflake]
    premium_subscriber: Optional[None]
    subscription_listing_id: Optional[Snowflake]
    available_for_purchase: Optional[None]
    guild_connections: Optional[None]


class Role(TypedDict):
    id: Snowflake
    name: str
    color: int
    hoist: bool
    icon: Optional[str]
    unicode_emoji: Optional[str]
    position: int
    permissions: Optional[str]
    managed: bool
    mentionable: bool
    tags: Optional[RoleTag]
    flags: int
