from __future__ import annotations

from typing import Any, List, TypedDict, TYPE_CHECKING

if TYPE_CHECKING:
    from typing_extensions import NotRequired

__all__ = ("User", "Member")


class User(TypedDict):
    id: int
    username: str
    discriminator: str
    avatar: NotRequired[str]
    avatar_decoration: NotRequired[str]
    bot: NotRequired[bool]
    bio: NotRequired[str]
    system: NotRequired[bool]
    mfa_enabled: NotRequired[bool]
    banner: NotRequired[str]
    ancent_color: NotRequired[int]
    locale: NotRequired[str]
    verified: NotRequired[bool]
    email: NotRequired[str]
    flags: NotRequired[int]
    premium_type: NotRequired[int]
    public_flags: NotRequired[int]


class Member(TypedDict):
    user: NotRequired[User]
    nick: NotRequired[str]
    avatar: NotRequired[str]
    roles: List[Any]
    joined_at: Any
    premium_since: NotRequired[Any]
    deaf: bool
    mute: bool
    flags: Any
    pending: NotRequired[bool]
    permissions: Any
    communication_disabled_until: NotRequired[Any]
