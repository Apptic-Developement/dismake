from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from .snowflake import Snowflake
    from typing_extensions import NotRequired


__all__ = ("UserData",)


class UserData(typing.TypedDict):
    id: Snowflake
    username: str
    discriminator: str
    global_name: typing.Optional[str]
    avatar: typing.Optional[str]
    bot: bool
    system: NotRequired[bool]
    mfa_enabled: NotRequired[bool]
    banner: NotRequired[typing.Optional[str]]
    accent_color: NotRequired[typing.Optional[int]]
    locale: NotRequired[str]
    verified: NotRequired[bool]
    email: NotRequired[typing.Optional[str]]
    flags: NotRequired[int]
    premium_type: NotRequired[int]
    public_flags: NotRequired[int]
    avatar_decoration: NotRequired[str]