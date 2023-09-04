from __future__ import annotations

from enum import IntEnum, IntFlag
from typing import TYPE_CHECKING, Any, Optional, Sequence, Tuple

from .color import Color

if TYPE_CHECKING:
    from dismake import Client
    from dismake.types import UserData


__all__: Sequence[str] = ("PartialUser", "User")


class PublicUserFlags(IntFlag):
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


class PremiumType(IntEnum):
    """The types of Nitro."""

    NONE = 0
    """No premium."""

    NITRO_CLASSIC = 1
    """Premium including basic perks like animated emojis and avatars."""

    NITRO = 2
    """Premium including all perks (e.g. 2 server boosts)."""


class PartialUser:
    """Represents a Partial User

    Parameters
    ----------
    client: Client
        The client application that models may use for procedures.
    id: int
        The unique ID of the user.

    Attributes
    ----------
    client: Client
        The client application that models may use for procedures.
    id: int
        The unique ID of the user.
    """

    def __init__(self, client: Client, id: int) -> None:
        self.client = client
        self.id = id

    @property
    def mention(self) -> str:
        """Return a raw mention string for the user."""
        return f"<@{self.id}>"


class User(PartialUser):
    """Represents a Discord user.

    Parameters
    ----------
    client: Client
        The client application that models may use for procedures.
    data: UserData
        The data payload containing user information.

    Attributes
    ----------
    username: str
        The username of the user.
    discriminator: str
        The discriminator of the user. (Legacy concept)
    global_name: Optional[str]
        The user's global nickname, taking precedence over the username in display.
    avatar: Optional[str]
        The hash of the user's avatar if present; otherwise, None.
    bot: bool
        Indicates whether the user is a bot account.
    system: bool
        Indicates whether the user represents Discord officially (system user).
    mfa_enabled: bool
        Indicates whether two-factor authentication is enabled for the user.
    banner: Optional[str]
        The hash of the user's banner if present; otherwise, None.
    accent_color: Optional[int]
        The user's accent color if present; otherwise, None.
    locale: str
        The user's locale.
    verified: bool
        Indicates whether the user is verified.
    email: Optional[str]
        The user's email address, if available.
    flags: UserFlag
        Flags associated with the user.
    premium_type: PremiumType
        The user's premium type.
    avatar_decoration: str
        The hash of the user's avatar decoration.

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
        "username",
        "discriminator",
        "global_name",
        "avatar",
        "bot",
        "system",
        "mfa_enabled",
        "banner",
        "accent_color",
        "locale",
        "verified",
        "email",
        "public_flags",
        "premium_type",
        "avatar_decoration",
    )

    def __init__(self, client: Client, data: UserData) -> None:
        super().__init__(client=client, id=int(data["id"]))
        self.username: str = data["username"]
        self.discriminator: str = data["discriminator"]
        self.global_name: Optional[str] = data.get("global_name")
        self.avatar: Optional[str] = data.get("avatar")
        self.bot: bool = data["bot"]
        self.system: bool = data["system"]
        self.mfa_enabled: bool = data["mfa_enabled"]
        self.banner: Optional[str] = data.get("banner")
        self.accent_color: Optional[Color] = (
            Color(value) if (value := data.get("accent_color")) is not None else None
        )
        self.locale: str = data["locale"]
        self.verified: bool = data["verified"]
        self.email: Optional[str] = data.get("email")
        self.public_flags: PublicUserFlags = PublicUserFlags(int(data.get("flags", 0)))
        self.premium_type: PremiumType = PremiumType(int(data["premium_type"]))
        self.avatar_decoration: str = data["avatar_decoration"]

    def __str__(self) -> str:
        return self.username

    def __repr__(self) -> str:
        return f"User(id={self.id}, username={self.username})"

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, User) and self.id == other.id

    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)
