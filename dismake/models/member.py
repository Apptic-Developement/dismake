from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, List, Optional, Sequence, Tuple

from .permissions import Permissions
from .role import Role
from .user import User

if TYPE_CHECKING:
    from dismake import Client
    from dismake.types import Member as MemberPayload

__all__: Sequence[str] = ("Member",)


class Member(User):
    """
    Represents a guild member in Discord.

    Parameters:
    -----------
    client : Client
        Client application that models may use for procedures.

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
        The member's flags

    pending : bool
        Whether the guild member is pending acceptance. (For when the guild has Membership Screening enabled)

    communication_disabled_until : datetime
        The timestamp until which the member's ability to communicate is disabled.

    Properties:
    -----------
    user : Optional[User]
        Returns the associated User object for the guild member if available; otherwise, returns None.

    roles : Optional[List[Role]]
        Returns a list of Role objects representing the guild member's roles if available; otherwise, returns None.

    permissions : Optional[Permissions]
        Returns a Permissions object representing the guild member's permissions if available; otherwise, returns None.

    """

    __slots__: Tuple[str, ...] = (
        "_client",
        "_payload",
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

    def __init__(self, client: Client, payload: MemberPayload):
        self._client = client
        self._payload = payload
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
    def user(self) -> Optional[User]:
        if user_data := self._payload.get("user"):
            return User(self._client, user_data)
        return None

    @property
    def roles(self) -> Optional[List[Role]]:
        if roles_data := self._payload.get("roles"):
            return list(Role(self._client, i) for i in roles_data)

        return None

    @property
    def permissions(self) -> Optional[Permissions]:
        if (perms_data := self._payload.get("permissions")) is not None:
            return Permissions(int(perms_data))
        return None
