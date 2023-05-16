from __future__ import annotations
from typing import Any, Optional

from ..enums import DefaultAvatar
from ..asset import Asset
from ..flags import UserFlags, GuildMemberFlags
from ..permissions import Permissions
from pydantic import BaseModel

__all__ = ("User", "Member")


class User(BaseModel):
    id: int
    username: str
    discriminator: str
    avatar: Optional[str]
    avatar_decoration: Optional[str]
    bot: Optional[bool]
    bio: Optional[str]
    system: Optional[bool]
    mfa_enabled: Optional[bool]
    banner: Optional[str]
    ancent_color: Optional[int]
    locale: Optional[str]
    verified: Optional[bool]
    email: Optional[str]
    flags: Optional[UserFlags]
    premium_type: Optional[int]
    public_flags: Optional[int]

    def __str__(self):
        return f"{self.username}#{self.discriminator}"

    @classmethod
    def from_resolved_data(cls, **kwargs):
        return cls(**kwargs)

    @property
    def mention(self) -> str:
        return f"<@{self.id}>"

    @property
    def display_avatar(self) -> Asset:
        if not self.avatar:
            return Asset.from_default_avatar(
                int(self.discriminator) % len(DefaultAvatar)
            )
        return Asset.from_avatar(self.avatar, self.id)


class Member(BaseModel):
    user: Optional[User]
    nick: Optional[str]
    avatar: Optional[str]
    roles: list[Any]
    joined_at: Any
    premium_since: Optional[Any]
    deaf: bool
    mute: bool
    flags: Optional[GuildMemberFlags]
    pending: Optional[bool]
    permissions: Optional[Permissions]
    communication_disabled_until: Optional[Any]

    def __str__(self) -> str:
        return f"{self.user}"