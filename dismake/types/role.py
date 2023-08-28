from __future__ import annotations
import typing

if typing.TYPE_CHECKING:
    from .snowflake import Snowflake
    from typing_extensions import NotRequired


__all__ = ("RoleData", "RoleTag")


class RoleTag(typing.TypedDict):
    bot_id: NotRequired[Snowflake]
    integration_id: NotRequired[Snowflake]
    premium_subscriber: NotRequired[None]
    subscription_listing_id: NotRequired[Snowflake]
    available_for_purchase: NotRequired[None]
    guild_connections: NotRequired[None]


class RoleData(typing.TypedDict):
    id: Snowflake
    name: str
    color: int
    hoist: bool
    icon: NotRequired[typing.Optional[str]]
    unicode_emoji: NotRequired[typing.Optional[str]]
    position: int
    permissions: str
    managed: bool
    mentionable: bool
    tags: NotRequired[RoleTag]
    flags: int
