from __future__ import annotations
from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from .snowflake import Snowflake
    from typing_extensions import NotRequired

__all__ = ("Role", "RoleTag")


class RoleTag(TypedDict):
    bot_id: NotRequired[Snowflake]
    integration_id: NotRequired[Snowflake]
    premium_subscriber: NotRequired[None]
    subscription_listing_id: NotRequired[Snowflake]
    available_for_purchase: NotRequired[None]
    guild_connections: NotRequired[None]


class Role(TypedDict):
    id: Snowflake
    name: str
    color: int
    hoist: bool
    icon: NotRequired[str]
    unicode_emoji: NotRequired[str]
    position: int
    permissions: NotRequired[str]
    managed: bool
    mentionable: bool
    tags: NotRequired[RoleTag]
    flags: int
