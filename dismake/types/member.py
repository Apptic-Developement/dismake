from __future__ import annotations

import typing


if typing.TYPE_CHECKING:
    from .user import UserData
    from datetime import datetime
    from .snowflake import Snowflake
    from typing_extensions import NotRequired

__all__ = ("MemberData",)


class MemberData(typing.TypedDict):
    user: typing.Optional[UserData]
    nick: typing.Optional[str]
    avatar: typing.Optional[str]
    roles: typing.List[Snowflake]
    joined_at: datetime
    premium_since: datetime
    deaf: bool
    mute: bool
    flags: bool
    pending: NotRequired[bool]
    permissions: NotRequired[typing.Optional[str]]
    communication_disabled_until: datetime