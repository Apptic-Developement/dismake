from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing_extensions import Self


__all__ = ("Asset",)


class AssetMixin:
    def __init__(self) -> None:
        pass


class Asset(AssetMixin):
    """Represent a CDN asset on Discord."""

    BASE = "https://cdn.discordapp.com"

    def __init__(self, *, url: str, key: str, animated: bool = False) -> None:
        self._url = url
        self._animated = animated
        self._key = key

    def __str__(self) -> str:
        return self._url

    @classmethod
    def from_default_avatar(cls, index: int) -> Self:
        return cls(
            url=f"{cls.BASE}/embed/avatars/{index}.png", key=str(index), animated=False
        )

    @classmethod
    def from_avatar(cls, avatar_hash: str, user_id: int) -> Self:
        animated = avatar_hash.startswith("a_")
        format = "gif" if animated else "png"
        return cls(
            url=f"{cls.BASE}/avatars/{user_id}/{avatar_hash}.{format}/?size=1024",
            animated=animated,
            key=avatar_hash,
        )

    @classmethod
    def from_guild_banner(cls, banner_hash: str, guild_id: int) -> Self:
        animated = banner_hash.startswith("a_")
        format = "gif" if animated else "png"
        return cls(
            url=f"{cls.BASE}/banners/{guild_id}/{banner_hash}.{format}",
            animated=animated,
            key=banner_hash,
        )

    @classmethod
    def from_guild_icon(cls, icon_hash: str, guild_id: int) -> Self:
        animated = icon_hash.startswith("a_")
        format = "gif" if animated else "png"
        return cls(
            url=f"{cls.BASE}/icons/{guild_id}/{icon_hash}.{format}",
            key=icon_hash,
            animated=animated,
        )
