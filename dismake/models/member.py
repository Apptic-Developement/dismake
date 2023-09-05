from __future__ import annotations

from enum import IntEnum
from typing import TYPE_CHECKING, List, Optional, Sequence, Tuple

from .permissions import Permissions
from .user import User
from ..utils import parse_time
from .asset import Asset
from .guild import PartialGuild

if TYPE_CHECKING:
    from dismake import Client
    from dismake.types import MemberData, Snowflake
    from datetime import datetime


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
    bot: bool
        Indicates whether the member is a bot account.
    system: bool
        Indicates whether the member represents Discord officially (system user).
    mfa_enabled: bool
        Indicates whether two-factor authentication is enabled for the member.
    accent_color: Optional[Color]
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
        "nickname",
        "_avatar",
        "roles",
        "joined_at",
        "premium_since",
        "deaf",
        "mute",
        "pending",
        "permissions",
        "communication_disabled_until",
        "flags",
    )

    def __init__(self, client: Client, guild_id: int, data: MemberData) -> None:
        super().__init__(client=client, data=data["user"])
        self.guild = PartialGuild(client=client, id=guild_id)
        self.nickname: Optional[str] = data.get("nick")
        self._avatar: Optional[str] = data.get("avatar")
        self.roles: List[Snowflake] = data.get("roles") or []
        self.joined_at: str = data["joined_at"]
        self.premium_since: Optional[datetime] = parse_time(data.get("premium_since"))
        self.deaf: bool = data["deaf"]
        self.mute: bool = data["mute"]
        self.pending: bool = data.get("pending", False)
        self.permissions: Permissions = Permissions.from_value(data.get("permissions"))
        self.communication_disabled_until: Optional[datetime] = parse_time(
            data.get("communication_disabled_until")
        )
        self.flags: MemberFlags = MemberFlags(int(data.get("flags", 0)))

    @property
    def guild_avatar(self) -> Optional[Asset]:
        """Returns an ``Asset`` for the guild avatar the member has."""
        if self._avatar is None:
            return None
        return Asset.from_guild_avatar(self.guild.id, self.id, self._avatar)

    @property
    def display_avatar(self) -> Asset:
        """Returns the member's display avatar.

        For regular members this is just their avatar, but
        if they have a guild specific avatar then that
        is returned instead.
        """
        return self.guild_avatar or self.avatar or self.default_avatar
