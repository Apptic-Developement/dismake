from __future__ import annotations

from typing import TYPE_CHECKING, Sequence, Optional

from dataclasses import dataclass, field


if TYPE_CHECKING:
    from typing_extensions import Self
    from ...types import EmbedAuthorData, EmbedFooterData, EmbedFieldData

__all__: Sequence[str] = ("EmbedAuthor", "EmbedFooter", "EmbedField")


@dataclass
class EmbedAuthor:
    name: Optional[str] = field(default=None, hash=True)
    url: Optional[str] = field(default=None, hash=True)
    icon_url: Optional[str] = field(default=None, hash=True)
    proxy_icon_url: Optional[str] = field(default=None, hash=True)

    @classmethod
    def from_dict(cls, data: EmbedAuthorData) -> Self:
        return cls(
            name=data["name"],
            url=data.get("url"),
            icon_url=data.get("icon_url"),
            proxy_icon_url=data.get("proxy_icon_url"),
        )

    def to_dict(self) -> Optional[EmbedAuthorData]:
        if self.name is not None:
            base: EmbedAuthorData = {"name": self.name}
            if self.icon_url is not None:
                base["icon_url"] = self.icon_url

            if self.url is not None:
                base["url"] = self.url

            if self.proxy_icon_url is not None:
                base["proxy_icon_url"] = self.proxy_icon_url

            return base
        return None


@dataclass
class EmbedFooter:
    text: Optional[str] = field(default=None, hash=True)
    icon_url: Optional[str] = field(default=None, hash=True)
    proxy_icon_url: Optional[str] = field(default=None, hash=True)

    @classmethod
    def from_dict(cls, data: EmbedFooterData) -> Self:
        return cls(
            text=data["text"],
            icon_url=data.get("icon_url"),
            proxy_icon_url=data.get("proxy_icon_url"),
        )
    def to_dict(self) -> Optional[EmbedFooterData]:
        if self.text is not None:
            base: EmbedFooterData = {"text": self.text}
            if self.icon_url is not None:
                base["icon_url"] = self.icon_url

            if self.proxy_icon_url is not None:
                base["proxy_icon_url"] = self.proxy_icon_url

            return base
        return None


@dataclass
class EmbedField:
    name: Optional[str] = field(default=None, hash=True)
    value: Optional[str] = field(default=None, hash=True)
    inline: Optional[bool] = field(default=None, hash=True)

    @classmethod
    def from_dict(cls, data: EmbedFieldData) -> Self:
        return cls(name=data["name"], value=data["value"], inline=data.get("inline"))

    def to_dict(self) -> Optional[EmbedFieldData]:
        if self.name is not None and self.value is not None:
            base: EmbedFieldData = {"name": self.name, "value": self.value}
            if self.inline is not None:
                base["inline"] = self.inline

            return base
        return None