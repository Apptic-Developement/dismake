from __future__ import annotations

import attrs
import typing

from .user import User, UserFlag, PremiumType

if typing.TYPE_CHECKING:
    from dismake import Client
    from typing_extensions import Self
    from dismake.types import MemberData, Snowflake
    from datetime import datetime


__all__: typing.Sequence[str] = ("Member",)


@attrs.define(kw_only=True, hash=True, weakref_slot=False)
class Member(User):
    """Represents a guild member."""

    guild_id: Snowflake = attrs.field(repr=True)
    """The ID of the guild this member belongs to."""

    is_deaf: bool = attrs.field(repr=False)
    """`True` if this member is deafened in the current voice channel"""

    is_mute: bool = attrs.field(repr=False)
    """`True` if this member is muted in the current voice channel."""

    is_pending: bool = attrs.field(repr=False)
    """Whether the user has passed the guild's membership screening requirements"""

    joined_at: datetime = attrs.field(repr=True)
    """The datetime of when this member joined the guild they belong to."""

    nickname: typing.Optional[str] = attrs.field(repr=True)
    """This member's nickname.

    This will be `None` if not set.
    """

    premium_since: typing.Optional[datetime] = attrs.field(repr=False)
    """The datetime of when this member started "boosting" this guild.

    Will be `None` if the member is not a premium user.
    """

    raw_communication_disabled_until: typing.Optional[datetime] = attrs.field(
        repr=False
    )
    """The datetime when this member's timeout will expire.

     Will be `None` if the member is not timed out.

     .. note::
        The datetime might be in the past, so it is recommended to use
        `communication_disabled_until` method to check if the member is timed
        out at the time of the call.
     """

    role_ids: typing.Sequence[Snowflake] = attrs.field(repr=False)
    """A sequence of the IDs of the member's current roles."""

    guild_avatar_hash: typing.Optional[str] = attrs.field(
        eq=False, hash=False, repr=False
    )
    """Hash of the member's guild avatar guild if set, else `None`.

    .. note::
        This takes precedence over `Member.avatar_hash`.
    """

    @property
    def communication_disabled_until(self) -> datetime:
        raise NotImplementedError

    @classmethod
    def deserialize_member(
        cls, client: Client, guild_id: Snowflake, data: MemberData
    ) -> Self:
        user = data["user"]
        return cls(
            client=client,
            id=user["id"],
            username=user["username"],
            global_name=user.get("global_name"),
            avatar_hash=user.get("avatar"),
            is_bot=user.get("bot", False),
            is_system=user.get("system", False),
            is_mfa_enabled=user.get("mfa_enabled", False),
            is_verified=user.get("verified", False),
            banner_hash=user.get("banner"),
            accent_color=user.get("accent_color"),
            locale=user.get("locale"),
            email=user.get("email"),
            flags=UserFlag(int(user.get("flags", 0))),
            premium_type=PremiumType(int(user.get("premium_type", 0))),
            avatar_decoration=user.get("avatar_decoration"),
            guild_id=guild_id,
            nickname=data.get("nick"),
            guild_avatar_hash=data.get("avatar"),
            joined_at=data["joined_at"],
            premium_since=data["premium_since"],
            is_deaf=data.get("deaf", False),
            is_mute=data.get("mute", False),
            is_pending=data.get("pending", False),
            role_ids=data.get("roles") or list(),
            raw_communication_disabled_until=data["communication_disabled_until"],
        )
