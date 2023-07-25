from __future__ import annotations
from typing import TYPE_CHECKING, Optional, TypedDict

if TYPE_CHECKING:
    from .snowflake import Snowflake

__all__ = (
    "Role",
)

class RoleTag(TypedDict):
    bot_id: Optional[Snowflake] 
    integration_id: Optional[Snowflake] 
    premium_subscriber: Optional[None] 
    subscription_listing_id: Optional[Snowflake] 
    available_for_purchase: Optional[None] 
    guild_connections: Optional[None] 

class Role(TypedDict):
    id: Snowflake	#snowflake	role id
    name: str	#string	role name
    color: int	#integer	integer representation of hexadecimal color code
    hoist: bool	#boolean	if this role is pinned in the user listing
    icon: Optional[str] #	?string	role icon hash
    unicode_emoji: Optional[str]#	?string	role unicode emoji
    position: int	#integer	position of this role
    permissions: Optional[str]	#string	permission bit set
    managed: bool	#boolean	whether this role is managed by an integration
    mentionable: bool	#boolean	whether this role is mentionable
    tags: RoleTag #	role tags object	the tags this role has
    flags: int	#integer	role flags combined as a bitfield