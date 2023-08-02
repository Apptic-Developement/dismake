from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from fastapi import Request
from datetime import datetime

from .permissions import Permissions
from .user import User
from .role import Role

if TYPE_CHECKING:
    from ..types import Member as MemberPayload

__all__ = ("Member",)


class Member(User):
    """
    Represents a guild member in Discord.

    Parameters:
    -----------
    request : Request
        The FastAPI request object used for handling the Discord API request.

    payload : MemberPayload
        The payload data received from Discord representing the guild member.

    Attributes:
    -----------
    nick : Optional[str]
        The nickname of the guild member, if set.

    avatar : Optional[str]
        The avatar hash of the guild member, if set.

    joined_at : datetime
        The timestamp when the guild member joined the server.

    premium_since : datetime
        The timestamp when the guild member started boosting the server with Nitro.

    deaf : bool
        Whether the guild member is server-deafened.

    mute : bool
        Whether the guild member is server-muted.

    flags : bool
        The member's flags. (You may want to elaborate on the possible flags)

    pending : bool
        Whether the guild member is pending acceptance. (For when the guild has Membership Screening enabled)

    communication_disabled_until : datetime
        The timestamp until which the member's ability to communicate is disabled.

    Properties:
    -----------
    user : User | None
        Returns the associated User object for the guild member if available; otherwise, returns None.

    roles : list[Role] | None
        Returns a list of Role objects representing the guild member's roles if available; otherwise, returns None.

    permissions : Permissions | None
        Returns a Permissions object representing the guild member's permissions if available; otherwise, returns None.

    """

    __slots__: tuple[str, ...] = (
        "_request",
        "_data",
        "nick",
        "avatar",
        "joined_at",
        "premium_since",
        "deaf",
        "mute",
        "flags",
        "pending",
        "communication_disabled_until",
    )

    def __init__(self, request: Request, payload: MemberPayload):
        self._request = request
        self._data = payload
        self.nick: Optional[str] = payload.get("nick")
        self.avatar: Optional[str] = payload.get("avatar")
        self.joined_at: datetime = payload["joined_at"]
        self.premium_since: datetime = payload["premium_since"]
        self.deaf: bool = payload["deaf"]
        self.mute: bool = payload["mute"]
        self.flags: bool = payload["flags"]
        self.pending: bool = payload["pending"]
        self.communication_disabled_until: datetime = payload[
            "communication_disabled_until"
        ]

    @property
    def user(self) -> User | None:
        if user_data := self._data.get("user"):
            return User(self._request, user_data)
        return None

    @property
    def roles(self) -> list[Role] | None:
        if roles_data := self._data.get("roles"):
            return [Role(self._request, i) for i in roles_data]

        return None

    @property
    def permissions(self) -> Permissions | None:
        if perms_data := self._data.get("permissions"):
            return Permissions(perms_data)
        return None
