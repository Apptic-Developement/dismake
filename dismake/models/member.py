from __future__ import annotations

from typing import TYPE_CHECKING, List, Sequence, Optional, Tuple


from .permissions import Permissions
from .user import User
from enum import IntEnum

if TYPE_CHECKING:
    from dismake.types import MemberData, Snowflake
    from dismake import Client


__all__: Sequence[str] = ("Member",)


class MemberFlags(IntEnum):
    """The known guild member flags that represent various member states."""

    DID_REJOIN = 1 << 0
    """Member has left and rejoined the guild (false)"""
    COMPLETED_ONBOARDING = 1 << 1
    """Member has completed onboarding (false)"""
    BYPASSES_VERIFICATION = 1 << 2
    """Member is exempt from guild verification requirements (true)"""
    STARTED_ONBOARDING = 1 << 3
    """Member has started onboarding (false)"""


class Member(User):
    """Represents a guild member within a Discord server.

    Parameters
    ----------
    client: Client
        The client application that manages this member.
    data: MemberData
        The data payload containing member information.

    Attributes
    ----------
    username: str
        The username of the member.
    id: int
        The unique ID of the member.
    discriminator: str
        The discriminator of the member. (Legacy concept)
    global_name: Optional[str]
        The member's global nickname, taking precedence over the username in display.
    avatar: Optional[str]
        The hash of the member's avatar if present; otherwise, None.
    bot: bool
        Indicates whether the member is a bot account.
    system: bool
        Indicates whether the member represents Discord officially (system user).
    mfa_enabled: bool
        Indicates whether two-factor authentication is enabled for the member.
    banner: Optional[str]
        The hash of the member's banner if present; otherwise, None.
    accent_color: Optional[int]
        The member's accent color if present; otherwise, None.
    locale: str
        The member's locale.
    verified: bool
        Indicates whether the member is verified.
    email: Optional[str]
        The member's email address, if available.
    flags: int
        Flags associated with the member.
    premium_type: int
        The member's premium type.
    public_flags: int
        Public flags associated with the member.
    avatar_decoration: str
        The hash of the member's avatar decoration.
    nickname: Optional[str]
        The nickname of the member within the guild.
    roles: List[Snowflake]
        List of role IDs that the member has.
    joined_at: datetime
        The date and time when the member joined the guild.
    premium_since: Optional[datetime]
        The date and time when the member became a premium subscriber.
    deaf: bool
        Indicates whether the member is deafened in voice channels.
    mute: bool
        Indicates whether the member is muted in voice channels.
    pending: bool
        Indicates whether the member has a pending invitation to the guild.
    permissions: Permissions
        The member's permissions within the guild.
    communication_disabled_until: datetime
        The date and time until which the member's communication is disabled.
    flags: MemberFlags
        Flags representing various member states.

    Operations
    ----------
    - ``x == y``:
        Checks if two users are equal.

    - ``x != y``:
        Checks if two users are not equal.

    - ``str(x)``:
        Returns the username.

    """

    __slots__: Tuple[str, ...] = (
        'nickname',
        'avatar',
        'roles',
        'joined_at',
        'premium_since',
        'deaf',
        'mute',
        'pending',
        'permissions',
        'communication_disabled_until',
        'flags',
    )

    def __init__(self, client: Client, data: MemberData) -> None:
        super().__init__(client=client, data=data["user"])
        self.nickname: Optional[str] = data.get("nick")
        self.avatar: Optional[str] = data.get("avatar")
        self.roles: List[Snowflake] = data.get("roles") or []
        self.joined_at: str = data["joined_at"]
        self.premium_since: Optional[str] = data.get("premium_since")
        self.deaf: bool = data["deaf"]
        self.mute: bool = data["mute"]
        self.pending: bool = data.get("pending", False)
        self.permissions: Permissions = Permissions.from_value(data.get("permissions"))
        self.communication_disabled_until: str = data["communication_disabled_until"]
        self.flags: MemberFlags = MemberFlags(int(data.get("flags", 0)))
