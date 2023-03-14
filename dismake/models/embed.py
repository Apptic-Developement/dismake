from __future__ import annotations
from typing import Literal, Optional
from datetime import datetime
from pydantic import BaseModel
from contextlib import suppress


class EmbedField(BaseModel):
    name: str
    value: str
    inline: bool


class EmbedFooter(BaseModel):
    text: str
    icon_url: Optional[str]
    proxy_icon_url: Optional[str]


class EmbedAsset(BaseModel):
    url: str
    proxy_url: Optional[str]
    height: Optional[int]
    width: Optional[int]


class EmbedProvider(BaseModel):
    name: Optional[str]
    url: Optional[str]


class EmbedAuthor(BaseModel):
    name: str
    url: Optional[str]
    icon_url: Optional[str]
    proxy_icon_url: Optional[str]


class Embed(BaseModel):
    title: Optional[str] = None
    type: Optional[
        Literal["rich", "image", "video", "gifv", "article", "link"]
    ] = "rich"
    description: Optional[str] = None
    url: Optional[str] = None
    timestamp: Optional[datetime] = None
    color: Optional[int] = None
    footer: Optional[EmbedFooter] = None
    fields: list[EmbedField] = []
    image: Optional[EmbedAsset] = None
    thumbnail: Optional[EmbedAsset] = None
    video: Optional[EmbedAsset] = None
    provider: Optional[EmbedProvider] = None
    author: Optional[EmbedAuthor] = None

    def add_field(self, name: str, value: str, inline: bool = True):
        self.fields.append(EmbedField(name=name, value=value, inline=inline))
        return self

    def get_field(self, index: int) -> Optional[EmbedField]:
        with suppress(IndexError):
            return self.fields[index]

    def set_footer(
        self, text: str, icon_url: Optional[str], proxy_icon_url: Optional[str]
    ):
        footer = {"text": text}
        if icon_url:
            footer["icon_url"] = icon_url
        if proxy_icon_url:
            footer["proxy_icon_url"] = proxy_icon_url
        self.footer = EmbedFooter(**footer)
        return self

    def set_image(
        self,
        url: str,
        proxy_url: Optional[str],
        width: Optional[int],
        height: Optional[int],
    ):
        self.image = EmbedAsset(
            url=url, proxy_url=proxy_url, width=width, height=height
        )
        return self

    def set_provider(self, name: str, url: str):
        self.provider = EmbedProvider(name=name, url=url)
        return self

    def set_author(
        self,
        name: str,
        url: Optional[str],
        icon_url: Optional[str],
        proxy_icon_url: Optional[str],
    ):
        self.author = EmbedAuthor(
            name=name, url=url, icon_url=icon_url, proxy_icon_url=proxy_icon_url
        )
        return self
