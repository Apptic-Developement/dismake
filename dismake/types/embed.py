from __future__ import annotations

from typing import List, Literal, Optional, Sequence, TypeAlias, TypedDict, Union
from typing_extensions import NotRequired


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
    text: Optional[str]
    icon_url: Optional[str]
    proxy_icon_url: Optional[str]


class EmbedImageData(TypedDict):
    url: str
    proxy_url: Optional[str]
    height: Optional[int]
    width: Optional[int]


class EmbedThumbnailData(TypedDict):
    url: str
    proxy_url: Optional[str]
    height: Optional[int]
    width: Optional[int]


class EmbedVideoData(TypedDict):
    url: Optional[str]
    proxy_url: Optional[str]
    height: Optional[int]
    width: Optional[int]


class EmbedProviderData(TypedDict):
    name: Optional[str]
    url: Optional[str]


class EmbedAuthorData(TypedDict):
    name: str
    url: NotRequired[Optional[str]]
    icon_url: NotRequired[Optional[str]]
    proxy_icon_url: NotRequired[Optional[str]]


class EmbedFieldData(TypedDict):
    name: str
    value: str
    inline: Optional[bool]


class EmbedData(TypedDict):
    title: NotRequired[Optional[str]]
    type: EmbedType
    description: NotRequired[Optional[str]]
    url: NotRequired[Optional[str]]
    timestamp: NotRequired[Optional[str]]
    color: NotRequired[Optional[int]]
    footer: NotRequired[Optional[EmbedFooterData]]
    image: NotRequired[Optional[EmbedImageData]]
    thumbnail: NotRequired[Optional[EmbedThumbnailData]]
    video: NotRequired[Optional[EmbedVideoData]]
    provider: NotRequired[Optional[EmbedProviderData]]
    author: NotRequired[Optional[EmbedAuthorData]]
    fields: NotRequired[Optional[List[EmbedFieldData]]]
