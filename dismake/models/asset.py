from __future__ import annotations

from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from typing_extensions import Self


__all__ = ("Asset",)

BASE_URL = "https://cdn.discordapp.com"


class Asset:
    """Represents a CDN asset on Discord.

    Parameters
    ----------
    url: str
        The url of the asset.
    hash: str
        The hash of the asset.
    animated: bool
        Wheather this asset is animated.

    Operations
    ----------
    - ``str(x)``:
        Returns the CDN URL of the asset.
    - ``len(x)``:
        Checks the length of the asset's URL.
    - ``repr(x)``:
        Returns a string representation of the asset.
    - ``x == y``:
        Checks if two Asset instances are equal.
    - ``x != y``:
        Checks if two Asset instances are not equal.

    """

    def __init__(self, url: str, hash: str, animated: bool) -> None:
        self._url = url
        self._hash = hash
        self._animated = animated

    @classmethod
    def from_default_avatar(cls, index: int) -> Self:
        return cls(
            url=f"{BASE_URL}/embed/avatars/{index}.png",
            hash=str(index),
            animated=False,
        )

    @classmethod
    def from_avatar(cls, user_id: int, avatar: str) -> Self:
        animated = avatar.startswith("a_")
        format = "gif" if animated else "png"
        return cls(
            url=f"{BASE_URL}/avatars/{user_id}/{avatar}.{format}?size=1024",
            hash=avatar,
            animated=animated,
        )

    @classmethod
    def from_guild_avatar(cls, guild_id: int, member_id: int, avatar: str) -> Self:
        animated = avatar.startswith("a_")
        format = "gif" if animated else "png"
        return cls(
            url=f"{BASE_URL}/guilds/{guild_id}/users/{member_id}/avatars/{avatar}.{format}?size=1024",
            hash=avatar,
            animated=animated,
        )

    @classmethod
    def from_icon(cls, object_id: int, icon_hash: str, path: str) -> Self:
        return cls(
            url=f"{BASE_URL}/{path}-icons/{object_id}/{icon_hash}.png?size=1024",
            hash=icon_hash,
            animated=False,
        )

    @classmethod
    def from_app_icon(
        cls, object_id: int, icon_hash: str, asset_type: Literal["icon", "cover_image"]
    ) -> Self:
        return cls(
            url=f"{BASE_URL}/app-icons/{object_id}/{asset_type}.png?size=1024",
            hash=icon_hash,
            animated=False,
        )

    @classmethod
    def from_cover_image(cls, object_id: int, cover_image_hash: str) -> Self:
        return cls(
            url=f"{BASE_URL}/app-assets/{object_id}/store/{cover_image_hash}.png?size=1024",
            hash=cover_image_hash,
            animated=False,
        )

    @classmethod
    def from_scheduled_event_cover_image(
        cls, scheduled_event_id: int, cover_image_hash: str
    ) -> Self:
        return cls(
            url=f"{BASE_URL}/guild-events/{scheduled_event_id}/{cover_image_hash}.png?size=1024",
            hash=cover_image_hash,
            animated=False,
        )

    @classmethod
    def from_guild_image(cls, guild_id: int, image: str, path: str) -> Self:
        animated = image.startswith("a_")
        format = "gif" if animated else "png"
        return cls(
            url=f"{BASE_URL}/{path}/{guild_id}/{image}.{format}?size=1024",
            hash=image,
            animated=animated,
        )

    @classmethod
    def from_guild_icon(cls, guild_id: int, icon_hash: str) -> Self:
        animated = icon_hash.startswith("a_")
        format = "gif" if animated else "png"
        return cls(
            url=f"{BASE_URL}/icons/{guild_id}/{icon_hash}.{format}?size=1024",
            hash=icon_hash,
            animated=animated,
        )

    @classmethod
    def from_sticker_banner(cls, banner: int) -> Self:
        return cls(
            url=f"{BASE_URL}/app-assets/710982414301790216/store/{banner}.png",
            hash=str(banner),
            animated=False,
        )

    @classmethod
    def from_user_banner(cls, user_id: int, banner_hash: str) -> Self:
        animated = banner_hash.startswith("a_")
        format = "gif" if animated else "png"
        return cls(
            url=f"{BASE_URL}/banners/{user_id}/{banner_hash}.{format}?size=512",
            hash=banner_hash,
            animated=animated,
        )

    def __str__(self) -> str:
        return self._url

    def __len__(self) -> int:
        return len(self._url)

    def __repr__(self) -> str:
        shorten = self._url.replace(BASE_URL, "")
        return f"<Asset url={shorten!r}>"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Asset) and self._url == other._url

    def __hash__(self) -> int:
        return hash(self._url)

    @property
    def url(self) -> str:
        """Returns the underlying URL of the asset."""
        return self._url

    @property
    def hash(self) -> str:
        """Returns the identifying hash of the asset."""
        return self._hash

    @property
    def is_animated(self) -> bool:
        """Returns whether the asset is animated."""
        return self._animated
