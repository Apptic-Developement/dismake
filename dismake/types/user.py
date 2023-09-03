from __future__ import annotations
from typing import TYPE_CHECKING, Optional, TypedDict

if TYPE_CHECKING:
    from .snowflake import Snowflake


__all__ = ("UserData",)


class UserData(TypedDict):
    id: Snowflake
    username: str
    discriminator: str
    global_name: Optional[str]
    avatar: Optional[str]
    bot: bool
    system: bool
    mfa_enabled: bool
    banner: Optional[str]
    accent_color: Optional[int]
    locale: str
    verified: bool
    email: Optional[str]
    flags: int
    premium_type: int
    public_flags: int
    avatar_decoration: str
