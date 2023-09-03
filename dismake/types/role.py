from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Sequence, TypedDict
from typing_extensions import NotRequired

if TYPE_CHECKING:
    from .snowflake import Snowflake

__all__: Sequence[str] = ("RoleTagsData", "RoleData")


class RoleTagsData(TypedDict):
    bot_id: Optional[Snowflake]
    integration_id: Optional[Snowflake]
    premium_subscriber: NotRequired[None]
    subscription_listing_id: Optional[Snowflake]
    available_for_purchase: NotRequired[None]
    guild_connections: NotRequired[None]


class RoleData(TypedDict):
    id: Snowflake
    name: str
    color: int
    hoist: bool
    icon: Optional[str]
    unicode_emoji: Optional[str]
    position: int
    permissions: str
    managed: bool
    mentionable: bool
    tags: Optional[RoleTagsData]
    flags: int
