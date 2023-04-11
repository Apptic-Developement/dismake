from __future__ import annotations
from typing import Any, Optional

from pydantic import BaseModel
from ..types import SnowFlake

__all__ = ("Role",)


class RoleTags(BaseModel):
    bot_id: Optional[SnowFlake]
    integration_id: Optional[SnowFlake]
    premium_subscriber: Optional[Any]
    subscription_listing_id: Optional[SnowFlake]
    available_for_purchase: Optional[Any]
    guild_connections: Optional[Any]


class Role(BaseModel):
    id: SnowFlake
    name: str
    color: int
    hoist: bool
    icon: Optional[str]
    unicode_emoji: Optional[str]
    position: int
    permissions: int
    managed: bool
    mentionable: bool
    tags: Optional[RoleTags]

    def __str__(self) -> str:
        return self.name

    @property
    def mention(self) -> str:
        return f"<@&{self.id}>"
