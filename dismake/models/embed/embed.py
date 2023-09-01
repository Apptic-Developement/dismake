from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Sequence, Tuple, Type


from .proxys import EmbedAuthor, EmbedField, EmbedFooter

if TYPE_CHECKING:
    from typing_extensions import Self
    from ...types import EmbedData, EmbedType


__all__: Sequence[str] = ("Embed",)


class Embed:
    """Represents an discord embed."""

    __slots__: Tuple[str, ...] = (
        "title",
        "description",
        "type",
        "url",
        "timestamp",
        "color",
        "_author",
        "_footer",
        "_fields",
    )

    def __init__(
        self,
        *,
        title: Any = None,
        description: Any = None,
        type: EmbedType = "rich",
        url: Any = None,
        timestamp: Any = None,
        color: Any = None,
    ) -> None:
        self.title = title
        self.description = description
        self.type = type
        self.url = url
        self.timestamp = timestamp
        self.color = color

    @classmethod
    def from_dict(cls, data: EmbedData) -> Self:
        embed = cls.__new__(cls)

        (
            embed.title,
            embed.description,
            embed.type,
            embed.url,
            embed.color,
            embed.timestamp,
        ) = (
            data.get("title"),
            data.get("description"),
            data["type"],
            data.get("url"),
            data.get("color"),
            data.get("timestamp"),
        )


        # attrs: Dict[str, Type[object]] = (
        #     "author": EmbedAuthor,
        #     "footer": EmbedFooter
        # )
        # for attr_name, attr_class in attrs.items():
        #     if (attr_data := data.get(attr)) is not None:
        #         ...
        # TODO
        return embed

    def to_dict(self) -> EmbedData:
        return NotImplemented

    def __str__(self) -> str:
        return f"Embed(title={self.title}, color={self.color}, fields={10})"

    def copy(self) -> Self:
        return self.from_dict(self.to_dict())

    @property
    def author(self) -> EmbedAuthor:
        return getattr(self, "_author", EmbedAuthor())

    def set_author(
        self,
        name: Optional[str] = None,
        *,
        url: Optional[str] = None,
        icon_url: Optional[str] = None,
        proxy_icon_url: Optional[str] = None,
    ) -> Self:
        if name is None:
            self._author = None

        else:
            self._author = EmbedAuthor(
                name=name, url=url, icon_url=icon_url, proxy_icon_url=proxy_icon_url
            )
        return self

    def remove_author(self) -> Self:
        self._author = None
        return self

    @property
    def footer(self) -> EmbedFooter:
        return getattr(self, "_footer", EmbedFooter())

    def set_footer(
        self,
        text: Optional[str] = None,
        *,
        icon_url: Optional[str] = None,
        proxy_icon_url: Optional[str] = None,
    ) -> Self:
        if text is None:
            self._footer = None

        else:
            self._footer = EmbedFooter(
                text=text, icon_url=icon_url, proxy_icon_url=proxy_icon_url
            )
        return self

    def remove_footer(self) -> Self:
        self._footer = None
        return self

    @property
    def fields(self) -> List[EmbedField]:
        return getattr(self, "_fields", [])

    def add_field(self, name: str, value: str, inline: Optional[bool] = None) -> Self:
        if not getattr(self, '_fields', None):
            self._fields = []
        
        self.fields.append(EmbedField(name=name, value=value, inline=inline))
        return self
    

