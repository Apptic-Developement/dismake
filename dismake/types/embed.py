from __future__ import annotations

import typing


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
    url: typing.Optional[str]
    icon_url: typing.Optional[str]
    proxy_icon_url: typing.Optional[str]

class EmbedFieldData(typing.TypedDict):
    name: str
    value: str
    inline: typing.Optional[bool]

class EmbedData(typing.TypedDict):
    title: typing.Optional[str]
    type: typing.Optional[str]
    description: typing.Optional[str]
    url: typing.Optional[str]
    timestamp: typing.Optional[str]
    color: typing.Optional[int]
    footer: typing.Optional[EmbedFooterData]
    image: typing.Optional[EmbedImageData]
    thumbnail: typing.Optional[EmbedThumbnailData]
    video: typing.Optional[EmbedVideoData]
    provider: typing.Optional[EmbedProviderData]
    author: typing.Optional[EmbedAuthorData]
    fields: typing.Optional[typing.List[EmbedFieldData]]