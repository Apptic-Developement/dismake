from __future__ import annotations

import typing
from contextlib import suppress

if typing.TYPE_CHECKING:
    from datetime import datetime
    from typing_extensions import Self
    from dismake.types import EmbedData

    class _EmbedFooterProxy(typing.Protocol):
        text: typing.Optional[str]
        icon_url: typing.Optional[str]

    class _EmbedFieldProxy(typing.Protocol):
        name: typing.Optional[str]
        value: typing.Optional[str]
        inline: bool

    class _EmbedMediaProxy(typing.Protocol):
        url: typing.Optional[str]
        proxy_url: typing.Optional[str]
        height: typing.Optional[int]
        width: typing.Optional[int]

    class _EmbedVideoProxy(typing.Protocol):
        url: typing.Optional[str]
        height: typing.Optional[int]
        width: typing.Optional[int]

    class _EmbedProviderProxy(typing.Protocol):
        name: typing.Optional[str]
        url: typing.Optional[str]

    class _EmbedAuthorProxy(typing.Protocol):
        name: typing.Optional[str]
        url: typing.Optional[str]
        icon_url: typing.Optional[str]
        proxy_icon_url: typing.Optional[str]


__all__: typing.Sequence[str] = ("Embed",)


EmbedType = typing.Literal["rich", "image", "video", "gifv", "article", "link"]


class EmbedProxy:
    def __init__(self, layer: typing.Dict[str, typing.Any]):
        self.__dict__.update(layer)

    def __len__(self) -> int:
        return len(self.__dict__)

    def __repr__(self) -> str:
        inner = ", ".join(
            (f"{k}={v!r}" for k, v in self.__dict__.items() if not k.startswith("_"))
        )
        return f"EmbedProxy({inner})"

    def __getattr__(self, attr: str) -> None:
        return None

    def __eq__(self, other: object) -> bool:
        return isinstance(other, EmbedProxy) and self.__dict__ == other.__dict__


class Embed:
    """Represents a Discord embed.

    Attributes
    -----------
    title: Optional[str]
        The title of the embed.
        This can be set during initialisation.
        Can only be up to 256 characters.
    type: str
        The type of embed. Usually "rich".
        This can be set during initialisation.
        Possible strings for embed types can be found on discord's
    description: Optional[str]
        The description of the embed.
        This can be set during initialisation.
        Can only be up to 4096 characters.
    url: Optional[str]
        The URL of the embed.
        This can be set during initialisation.
    timestamp: Optional[datetime]
        The timestamp of the embed content. This is an aware datetime.
        If a naive datetime is passed, it is converted to an aware
        datetime with the local timezone.
    color: Optional[Union[str, int]]
        The colour code of the embed.
        This can be set during initialisation.
    """

    def __init__(
        self,
        title: typing.Optional[str],
        description: typing.Optional[str],
        url: typing.Optional[str],
        timestamp: typing.Optional[datetime],
        color: typing.Optional[typing.Union[str, int]],
        type: EmbedType = "rich",
    ) -> None:
        self.title = title
        self.type = type
        self.description = description
        self.url = url
        self.timestamp = timestamp
        self.color = color

    @classmethod
    def from_dict(cls, data: EmbedData) -> Embed:
        raise NotImplementedError

    def to_dict(self) -> EmbedData:
        raise NotImplementedError

    @property
    def footer(self) -> _EmbedFooterProxy:
        return EmbedProxy[_EmbedFooterProxy](getattr(self, "_footer", {}))  # type: ignore

    def set_footer(
        self, text: typing.Optional[str], *, icon_url: typing.Optional[str]
    ) -> Self:
        self._footer: typing.Dict[str, str] = {}
        if text is not None:
            self._footer["text"] = str(text)

        if icon_url is not None:
            self._footer["icon_url"] = str(icon_url)

        return self

    def remove_footer(self) -> Self:
        with suppress(AttributeError):
            del self._footer
        return self
