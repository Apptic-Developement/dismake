from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from .snowflake import Snowflake
    from typing_extensions import NotRequired


__all__ = ("User",)


class User(TypedDict):
    id: Snowflake
    username: str
    discriminator: str
    global_name: NotRequired[str]
    avatar: NotRequired[str]
    bot: bool
    system: NotRequired[bool]
    mfa_enabled: NotRequired[bool]
    banner: NotRequired[str]
    accent_color: NotRequired[int]
    locale: NotRequired[str]
    verified: NotRequired[bool]
    email: NotRequired[str]
    flags: NotRequired[int]
    premium_type: NotRequired[int]
    public_flags: NotRequired[int]
    avatar_decoration: NotRequired[str]
