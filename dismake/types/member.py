from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, TypedDict


if TYPE_CHECKING:
    from .user import UserData
    from .snowflake import Snowflake
    from typing_extensions import NotRequired

__all__ = ("MemberData",)


class MemberData(TypedDict):
    user: UserData
    nick: NotRequired[Optional[str]]
    avatar: NotRequired[Optional[str]]
    roles: List[Snowflake]
    joined_at: str
    premium_since: NotRequired[Optional[str]]
    deaf: bool
    mute: bool
    flags: str
    pending: NotRequired[bool]
    permissions: NotRequired[str]
    communication_disabled_until: str
