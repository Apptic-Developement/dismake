from __future__ import annotations

from typing import TYPE_CHECKING, Optional, TypedDict

if TYPE_CHECKING:
    from .user import User
    from datetime import datetime
    from .role import Role

__all__ = ("Member",)


class Member(TypedDict):
    user: Optional[User]
    nick: Optional[str]
    avatar: Optional[str]
    roles: Optional[list[Role]]
    joined_at: datetime
    premium_since: datetime
    deaf: bool
    mute: bool
    flags: bool
    pending: bool
    permissions: Optional[str]
    communication_disabled_until: datetime
