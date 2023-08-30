from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, TypedDict


if TYPE_CHECKING:
    from .user import UserData
    from datetime import datetime
    from .snowflake import Snowflake

__all__ = ("MemberData",)


class MemberData(TypedDict):
    user: UserData
    nick: Optional[str]
    avatar: Optional[str]
    roles: Optional[List[Snowflake]]
    joined_at: datetime
    premium_since: Optional[datetime]
    deaf: bool
    mute: bool
    flags: str
    pending: bool
    permissions: str
    communication_disabled_until: datetime