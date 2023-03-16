from __future__ import annotations
from typing import Any, Optional

from dismake.enums import DefaultAvatar
from ..asset import Asset

from pydantic import BaseModel


__all__ = ("User", "Member")

FLAGS_MAPPING = {
    1 << 0: "STAFF",
    1 << 1: "PARTNER",
    1 << 2: "HYPESQUAD",
    1 << 3: "BUG_HUNTER_LEVEL_1",
    1 << 6: "HYPESQUAD_ONLINE_HOUSE_1",
    1 << 7: "HYPESQUAD_ONLINE_HOUSE_2",
    1 << 8: "HYPESQUAD_ONLINE_HOUSE_3",
    1 << 9: "PREMIUM_EARLY_SUPPORTER",
    1 << 10: "TEAM_PSEUDO_USER",
    1 << 14: "BUG_HUNTER_LEVEL_2",
    1 << 16: "VERIFIED_BOT",
    1 << 17: "VERIFIED_DEVELOPER",
    1 << 18: "CERTIFIED_MODERATOR",
    1 << 19: "BOT_HTTP_INTERACTIONS",
    1 << 22: "ACTIVE_DEVELOPER",
}


class User(BaseModel):
    id: int
    username: str
    display_name: Optional[str]
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
    email: Optional[str | None]
    flags: Optional[int]
    premium_type: Optional[int]
    public_flags: Optional[int]

    def __str__(self):
        return f"{self.username}#{self.discriminator}"

    @property
    def get_flags(self) -> Optional[list[str | None]]:
        _flag_names = list()
        for k, v in FLAGS_MAPPING.items():
            if k == self.flags:
                _flag_names.append(v)

        return _flag_names

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
    flags: Any
    pending: Optional[bool]
    permissions: Any
    communication_disabled_until: Optional[Any]

    def __str__(self) -> str:
        return f"{self.user}"
