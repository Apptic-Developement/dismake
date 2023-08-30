from __future__ import annotations

from typing import List, Literal, Sequence, TypedDict, Union
from typing_extensions import NotRequired, TypeAlias


__all__: Sequence[str] = (
    "EmbedFooterData",
    "EmbedImageData",
    "EmbedThumbnailData",
    "EmbedVideoData",
    "EmbedProviderData",
    "EmbedAuthorData",
    "EmbedFieldData",
    "EmbedType",
    "EmbedData",
)

EmbedType: TypeAlias = Union[
    Literal["rich", "image", "video", "gifv", "article", "link"], str
]


class EmbedFooterData(TypedDict):
    text: str
    icon_url: NotRequired[str]
    proxy_icon_url: NotRequired[str]

class _EmbedAttachment(TypedDict):
    url: str
    proxy_url: NotRequired[str]
    height: NotRequired[int]
    width: NotRequired[int]

class EmbedImageData(_EmbedAttachment):
    pass

class EmbedThumbnailData(_EmbedAttachment):
    pass


class EmbedVideoData(TypedDict):
    url: NotRequired[str]
    proxy_url: NotRequired[str]
    height: NotRequired[int]
    width: NotRequired[int]


class EmbedProviderData(TypedDict):
    name: NotRequired[str]
    url: NotRequired[str]


class EmbedAuthorData(TypedDict):
    name: str
    url: NotRequired[str]
    icon_url: NotRequired[str]
    proxy_icon_url: NotRequired[str]


class EmbedFieldData(TypedDict):
    name: str
    value: str
    inline: NotRequired[bool]


class EmbedData(TypedDict):
    title: NotRequired[str]
    type: EmbedType
    description: NotRequired[str]
    url: NotRequired[str]
    timestamp: NotRequired[str]
    color: NotRequired[int]
    footer: NotRequired[EmbedFooterData]
    image: NotRequired[EmbedImageData]
    thumbnail: NotRequired[EmbedThumbnailData]
    video: NotRequired[EmbedVideoData]
    provider: NotRequired[EmbedProviderData]
    author: NotRequired[EmbedAuthorData]
    fields: NotRequired[List[EmbedFieldData]]
