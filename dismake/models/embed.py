from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Optional, Sequence, Tuple, Type
from dataclasses import dataclass, field

from dismake.types.embed import EmbedAuthorData, EmbedFieldData, EmbedFooterData

if TYPE_CHECKING:
    from typing_extensions import Self
    from ..types import EmbedData, EmbedType

__all__: Sequence[str] = ("Embed",)


@dataclass()
class EmbedAuthor:
    name: Optional[str] = field(default=None, hash=True)
    url: Optional[str] = field(default=None, hash=True)
    icon_url: Optional[str] = field(default=None, hash=True)
    proxy_icon_url: Optional[str] = field(default=None, hash=True)

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


@dataclass()
class EmbedFooter:
    text: Optional[str] = field(default=None, hash=True)
    icon_url: Optional[str] = field(default=None, hash=True)
    proxy_icon_url: Optional[str] = field(default=None, hash=True)

    def to_dict(self) -> Optional[EmbedFooterData]:
        if self.text is not None:
            base: EmbedFooterData = {"text": self.text}
            if self.icon_url is not None:
                base["icon_url"] = self.icon_url

            if self.proxy_icon_url is not None:
                base["proxy_icon_url"] = self.proxy_icon_url

            return base
        return None


@dataclass()
class EmbedField:
    name: Optional[str] = field(default=None, hash=True)
    value: Optional[str] = field(default=None, hash=True)
    inline: Optional[bool] = field(default=None, hash=True)

    def to_dict(self) -> Optional[EmbedFieldData]:
        if self.name is not None and self.value is not None:
            base: EmbedFieldData = {"name": self.name, "value": self.value}
            if self.inline is not None:
                base["inline"] = self.inline

            return base
        return None


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
        # Create a new instance of the class
        embed = cls.__new__(cls)

        # Set the 'type' attribute from the data dictionary
        embed.type = data["type"]

        # Loop through specified fields and set them as attributes of the embed object
        for field in ("title", "description", "url", "color"):
            setattr(embed, field, data.get(field))

        # Set the 'timestamp' attribute from the data dictionary
        embed.timestamp = data.get(
            "timestamp"
        )  # TODO: Consider how to handle 'timestamp'

        # Define a dictionary mapping attribute names to their corresponding classes
        attrs: Dict[str, Type[Any]] = {"author": EmbedAuthor, "footer": EmbedFooter}

        # Loop through attributes defined in the 'attrs' dictionary
        for attr_name, attr_class in attrs.items():
            # Check if the attribute exists in the data dictionary
            if (attr_data := data.get(attr_name)) is not None:
                # Create an instance of the attribute class using data
                attr_instance = attr_class(**attr_data)
                # Set the attribute in the new embed object with a prefixed name (e.g., self._author)
                setattr(embed, "_" + attr_name, attr_instance)

        return embed

    def to_dict(self) -> EmbedData:
        # Create a base dictionary with the 'type' attribute
        base: EmbedData = {"type": self.type}

        # Iterate through all the attributes defined in __slots__
        for attr in self.__slots__:
            # Check if the attribute name starts with an underscore ('_') indicating
            # it's an embed attribute (e.g., _author, _footer)
            if attr.startswith("_"):
                try:
                    # Fetch the attribute
                    fetched_attr = getattr(self, attr)
                except AttributeError:
                    pass
                else:
                    # Convert the fetched attribute to a dictionary using its to_dict method
                    # and add it to our base dictionary.
                    # We use type: ignore here because mypy incorrectly flags this line due to dynamic key generation.
                    base[attr[1:]] = fetched_attr.to_dict()  # type: ignore

        # Check and add 'title' if it exists
        if self.title is not None:
            base["title"] = str(self.title)

        # Check and add 'description' if it exists
        if self.description is not None:
            base["description"] = str(self.description)

        # Check and add 'timestamp' if it exists
        if self.timestamp is not None:
            base["timestamp"] = str(self.timestamp)

        # Check and add 'color' if it exists
        if self.color is not None:
            base["color"] = self.color

        # Check and add 'url' if it exists
        if self.url is not None:
            base["url"] = self.url

        return base

    def __str__(self) -> str:
        return f"Embed(title={self.title}, color={self.color}, fields={10})"

    def copy(self) -> Self:
        return self.from_dict(self.to_dict())
