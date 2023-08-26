from __future__ import annotations

from typing import TYPE_CHECKING, Any

from enum import IntEnum, IntFlag


if TYPE_CHECKING:
    from dismake.types import User as UserPayload
    from typing import Optional
    from typing_extensions import Self


__all__ = ("User", "PartialUser")


class PremiumType(IntEnum):
    """The types of Nitro."""

    NONE = 0
    NITRO_CLASSIC = 1
    NITRO = 2
    NITRO_BASIC = 3


class UserFlags(IntFlag):
    """The known user flags that represent account badges."""

    STAFF = 1 << 0
    PARTNER = 1 << 1
    HYPESQUAD = 1 << 2
    BUG_HUNTER_LEVEL_1 = 1 << 3
    HYPESQUAD_ONLINE_HOUSE_1 = 1 << 6
    HYPESQUAD_ONLINE_HOUSE_2 = 1 << 7
    HYPESQUAD_ONLINE_HOUSE_3 = 1 << 8
    PREMIUM_EARLY_SUPPORTER = 1 << 9
    TEAM_PSEUDO_USER = 1 << 10
    BUG_HUNTER_LEVEL_2 = 1 << 14
    VERIFIED_BOT = 1 << 16
    VERIFIED_DEVELOPER = 1 << 17
    CERTIFIED_MODERATOR = 1 << 18
    BOT_HTTP_INTERACTIONS = 1 << 19
    ACTIVE_DEVELOPER = 1 << 22


class PartialUser:
    """
    Represents a partial Discord user.

    A partial user object contains only essential information about a user,
    typically used when the full user data is not required, such as in some API responses.

    Parameters
    -----------
    app: Any
        Client application that models may use for procedures.

    id: int
        The unique identifier (ID) of the user.

    Attributes
    -----------
    id: int
        The unique identifier (ID) of the user.

    """

    __slots__: tuple[str, ...] = ("_app", "id")

    def __init__(self, app: Any, id: int) -> None:
        self._app = app
        self.id: int = id


class User(PartialUser):
    """
    Represents a Discord user.

    This class inherits the `PartialUser` class to represent a complete Discord user.

    Parameters
    -----------
    app : Any
        Client application that models may use for procedures.

    payload : UserPayload
        The payload data received from Discord representing the user.

    Attributes
    -----------
    username : str
        The username of the user.

    discriminator : str
        The discriminator of the user (e.g., '1234' in 'User#1234').

    global_name : Optional[str]
        The user's global name if set.

    avatar : Optional[str]
        The avatar hash of the user, if set.

    bot : bool
        True if the user is a bot; otherwise, False.

    system : Optional[bool]
        True if the user is a Discord system user; otherwise, None.

    mfa_enabled : Optional[bool]
        True if the user has multi-factor authentication (MFA) enabled; otherwise, None.

    banner : Optional[str]
        The user's banner hash if set.

    accent_color : Optional[int]
        The user's accent color represented as an integer if set.

    locale : Optional[str]
        The user's locale if set.

    verified : Optional[bool]
        True if the user is verified; otherwise, None.

    email : Optional[str]
        The user's email address if set.

    premium_type : PremiumType
        The user's premium (Nitro) type, represented by a PremiumType enum.

    public_flags : Optional[UserFlags]
        The user's public flags, represented by a UserFlags enum if set.

    avatar_decoration : Optional[str]
        The user's avatar decoration hash if set.
    """

    __slots__: tuple[str, ...] = (
        "_payload" "username",
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
        "premium_type",
        "public_flags",
        "avatar_decoration",
    )

    def __init__(self, app: Any, payload: UserPayload):
        super().__init__(app=app, id=int(payload["id"]))
        self._payload = payload
        self.username: str = payload["username"]
        self.discriminator: str = payload["discriminator"]
        self.global_name: Optional[str] = payload.get("global_name")
        self.avatar: Optional[str] = payload.get("avatar")
        self.bot: bool = payload["bot"]
        self.system: Optional[bool] = payload.get("system")
        self.mfa_enabled: Optional[bool] = payload.get("mfa_enabled")
        self.banner: Optional[str] = payload.get("banner")
        self.accent_color: Optional[int] = payload.get("accent_color")
        self.locale: Optional[str] = payload.get("locale")
        self.verified: Optional[bool] = payload.get("verified")
        self.email: Optional[str] = payload.get("email")
        self.premium_type: PremiumType = PremiumType(payload.get("premium_type") or 0)
        self.public_flags: Optional[UserFlags] = UserFlags(
            payload.get("public_flags") or 0
        )
        self.avatar_decoration: Optional[str] = payload.get("avatar_decoration")

    def __eq__(self, obj: Self) -> bool:
        return self.id == obj.id
