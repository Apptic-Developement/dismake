from __future__ import annotations

from typing import TYPE_CHECKING, Optional, TypedDict
if TYPE_CHECKING:
    from .snowflake import Snowflake
    

__all__ = (
    "User",
)


class User(TypedDict):
    id: Snowflake
    username: str
    discriminator: str
    global_name: Optional[str]
    avatar: Optional[str]
    bot: bool
    system: Optional[bool]
    mfa_enabled: Optional[bool]
    banner: Optional[str]
    accent_color: Optional[int]
    locale: Optional[str]
    verified: Optional[bool]
    email: Optional[str]
    flags: Optional[int]
    premium_type: Optional[int]
    public_flags: Optional[int]
    avatar_decoration: Optional[str]
