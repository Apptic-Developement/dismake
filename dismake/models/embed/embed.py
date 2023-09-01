from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Any,
    List,
    Optional,
    Sequence,
    Tuple,
)

from dismake.types.embed import EmbedFieldData

from .proxys import EmbedAuthor, EmbedField, EmbedFooter

if TYPE_CHECKING:
    from typing_extensions import Self
    from ...types import EmbedData, EmbedType


__all__: Sequence[str] = ("Embed",)

from discord import Embed as EEEEEE

EEEEEE.from_dict


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

        if (author_data := data.get("author")) is not None:
            embed._author = EmbedAuthor.from_dict(author_data)

        if (footer_data := data.get("footer")) is not None:
            embed._footer = EmbedFooter.from_dict(footer_data)

        if (fields_data := data.get("fields")) is not None:
            temp_fields: List[EmbedField] = list()
            for field_data in fields_data:
                temp_fields.append(EmbedField.from_dict(field_data))

            embed._fields = temp_fields
        return embed

    def to_dict(self) -> EmbedData:
        # Create a base dictionary with the embed type
        base: EmbedData = {"type": self.type}

        # Loop through the slots to extract embed proxies
        for slot in self.__slots__:
            # Check if the slot represents an embed proxy (starts with '_')
            if slot.startswith("_"):
                # Get the value of the attribute
                attr_value = getattr(self, slot, None)
                # Check if the attribute is not None
                if attr_value is not None:
                    if slot == "_fields":
                        # Handle the "_fields" attribute differently by converting each field to a dictionary
                        temp_fields: List[EmbedFieldData] = list()
                        for field in attr_value:
                            temp_fields.append(field.to_dict())
                        base["fields"] = temp_fields
                    else:
                        # Remove the leading '_' from the slot name and set it as a key in the base dictionary
                        # Use the "to_dict()" method of the attribute to obtain a valid embed proxy dictionary
                        base[slot[1:]] = attr_value.to_dict()  # type: ignore  # Safe to ignore: Dynamically generated keys from __slots__

        # Check and add optional attributes if they are not None
        if self.title is not None:
            base["title"] = self.title

        if self.description is not None:
            base["description"] = self.description

        if self.color is not None:
            base["color"] = self.color

        if self.timestamp is not None:
            base["timestamp"] = self.timestamp

        if self.url is not None:
            base["url"] = self.url

        return base


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
        if not getattr(self, "_fields", None):
            self._fields: List[EmbedField] = []

        self.fields.append(EmbedField(name=name, value=value, inline=inline))
        return self
