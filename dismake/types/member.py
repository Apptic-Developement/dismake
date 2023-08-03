from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from .user import User
    from datetime import datetime
    from .role import Role
    from typing_extensions import NotRequired

__all__ = ("Member",)


class Member(TypedDict):
    user: NotRequired[User]
    nick: NotRequired[str]
    avatar: NotRequired[str]
    roles: NotRequired[list[Role]]
    joined_at: datetime
    premium_since: datetime
    deaf: bool
    mute: bool
    flags: bool
    pending: bool
    permissions: NotRequired[str]
    communication_disabled_until: datetime
