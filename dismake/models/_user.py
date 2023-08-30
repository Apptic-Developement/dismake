from __future__ import annotations

import typing
import attrs

from enum import IntEnum, IntFlag

if typing.TYPE_CHECKING:
    from dismake import Client
    from typing_extensions import Self
    from dismake.types import Snowflake, UserData


__all__: typing.Sequence[str] = ("PartialUser", "User")


@typing.final
class UserFlag(IntFlag):
    """The known user flags that represent account badges."""

    NONE = 0
    """None."""

    DISCORD_EMPLOYEE = 1 << 0
    """Discord Employee."""

    PARTNERED_SERVER_OWNER = 1 << 1
    """Owner of a partnered Discord server."""

    HYPESQUAD_EVENTS = 1 << 2
    """HypeSquad Events."""

    BUG_HUNTER_LEVEL_1 = 1 << 3
    """Bug Hunter Level 1."""

    HYPESQUAD_BRAVERY = 1 << 6
    """House of Bravery."""

    HYPESQUAD_BRILLIANCE = 1 << 7
    """House of Brilliance."""

    HYPESQUAD_BALANCE = 1 << 8
    """House of Balance."""

    EARLY_SUPPORTER = 1 << 9
    """Early Supporter."""

    TEAM_USER = 1 << 10
    """Team user."""

    BUG_HUNTER_LEVEL_2 = 1 << 14
    """Bug Hunter Level 2."""

    VERIFIED_BOT = 1 << 16
    """Verified Bot."""

    EARLY_VERIFIED_DEVELOPER = 1 << 17
    """Early verified Bot Developer.

    Only applies to users that verified their account before 20th August 2019.
    """

    DISCORD_CERTIFIED_MODERATOR = 1 << 18
    """Discord Certified Moderator."""

    BOT_HTTP_INTERACTIONS = 1 << 19
    """Bot uses only HTTP interactions and is shown in the active member list."""

    ACTIVE_DEVELOPER = 1 << 22
    """User is an active bot developer."""


@typing.final
class PremiumType(IntEnum):
    """The types of Nitro."""

    NONE = 0
    """No premium."""

    NITRO_CLASSIC = 1
    """Premium including basic perks like animated emojis and avatars."""

    NITRO = 2
    """Premium including all perks (e.g. 2 server boosts)."""


@attrs.define(kw_only=True, hash=True, weakref_slot=False)
class PartialUser:
    """Represents a partial discord user object."""

    client: Client = attrs.field(repr=False, eq=False, hash=False)
    """Client application that models may use for procedures."""

    id: Snowflake = attrs.field(hash=True)
    """The ID of this entity."""

    @property
    def mention(self) -> str:
        """Return a raw mention string for the given user."""
        return f"<@{self.id}>"


@attrs.define(kw_only=True, hash=True, weakref_slot=False)
class User(PartialUser):
    """Represents a discord user object."""

    username: str = attrs.field(hash=True)
    """Username of the user."""

    global_name: typing.Optional[str] = attrs.field(hash=True)
    """Global name for the user, if they have one, otherwise `None`."""

    avatar_hash: typing.Optional[str] = attrs.field(eq=False, hash=False, repr=False)
    """Hash of the user's avatar, if available."""

    is_bot: bool = attrs.field(eq=False, hash=False, repr=True)
    """Indicates whether the user is a bot."""

    is_system: bool = attrs.field(eq=False, hash=False, repr=True)
    """Indicates whether the user is a system user."""

    is_mfa_enabled: bool = attrs.field(eq=False, hash=False, repr=True)
    """Indicates whether the user has two-factor authentication enabled."""

    is_verified: bool = attrs.field(eq=False, hash=False, repr=True)
    """Indicates whether the user is verified."""

    banner_hash: typing.Optional[str] = attrs.field(eq=False, hash=False, repr=False)
    """Hash of the user's banner, if available."""

    accent_color: typing.Optional[int] = attrs.field(eq=False, hash=False, repr=False)
    """The user's accent color."""

    locale: typing.Optional[typing.Any] = attrs.field(eq=False, hash=False, repr=False)
    """The user's locale."""

    email: typing.Optional[str] = attrs.field(eq=False, hash=False, repr=False)
    """The user's email address, if available."""

    flags: UserFlag = attrs.field(eq=False, hash=False, repr=True)
    """Flags associated with the user."""

    premium_type: PremiumType = attrs.field(eq=False, hash=False, repr=True)
    """The user's premium type."""

    # public_flags: typing.Optional[int]
    # """Public flags associated with the user."""

    avatar_decoration: typing.Optional[str] = attrs.field(
        eq=False, hash=False, repr=False
    )
    """The user avatar decoration hash."""

    @classmethod
    def deserialize_user(cls, client: Client, data: UserData) -> Self:

        return cls(
            client=client,
            id=data["id"],
            username=data["username"],
            global_name=data.get("global_name"),
            avatar_hash=data.get("avatar"),
            is_bot=data.get("bot", False),
            is_system=data.get("system", False),
            is_mfa_enabled=data.get("mfa_enabled", False),
            is_verified=data.get("verified", False),
            banner_hash=data.get("banner"),
            accent_color=data.get("accent_color"),
            locale=data.get("locale"),
            email=data.get("email"),
            flags=UserFlag(int(data.get("flags", 0))),
            premium_type=PremiumType(int(data.get("premium_type", 0))),
            avatar_decoration=data.get("avatar_decoration"),
        )
