from __future__ import annotations

import typing
from typing_extensions import NotRequired


__all__: typing.Sequence[str] = (
    "EmbedFooterData",
    "EmbedImageData",
    "EmbedThumbnailData",
    "EmbedVideoData",
    "EmbedProviderData",
    "EmbedAuthorData",
    "EmbedFieldData",
    "EmbedData"

)
class EmbedFooterData(typing.TypedDict):
    text: typing.Optional[str]
    icon_url: typing.Optional[str]
    proxy_icon_url: typing.Optional[str]

class EmbedImageData(typing.TypedDict):
    url: str
    proxy_url: typing.Optional[str]
    height: typing.Optional[int]
    width: typing.Optional[int]

class EmbedThumbnailData(typing.TypedDict):
    url: str
    proxy_url: typing.Optional[str]
    height: typing.Optional[int]
    width: typing.Optional[int]

class EmbedVideoData(typing.TypedDict):
    url: typing.Optional[str]
    proxy_url: typing.Optional[str]
    height: typing.Optional[int]
    width: typing.Optional[int]

class EmbedProviderData(typing.TypedDict):
    name: typing.Optional[str]
    url: typing.Optional[str]

class EmbedAuthorData(typing.TypedDict):
    name: str
    url: NotRequired[typing.Optional[str]]
    icon_url: NotRequired[typing.Optional[str]]
    proxy_icon_url: NotRequired[typing.Optional[str]]

class EmbedFieldData(typing.TypedDict):
    name: str
    value: str
    inline: typing.Optional[bool]

class EmbedData(typing.TypedDict):
    title: NotRequired[typing.Optional[str]]
    type: str
    description: NotRequired[typing.Optional[str]]
    url: NotRequired[typing.Optional[str]]
    timestamp: NotRequired[typing.Optional[str]]
    color: NotRequired[typing.Optional[int]]
    footer: NotRequired[typing.Optional[EmbedFooterData]]
    image: NotRequired[typing.Optional[EmbedImageData]]
    thumbnail: NotRequired[typing.Optional[EmbedThumbnailData]]
    video: NotRequired[typing.Optional[EmbedVideoData]]
    provider: NotRequired[typing.Optional[EmbedProviderData]]
    author: NotRequired[typing.Optional[EmbedAuthorData]]
    fields: NotRequired[typing.Optional[typing.List[EmbedFieldData]]]