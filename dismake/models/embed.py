from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional, Sequence, Tuple
from dataclasses import dataclass, field

from dismake.types.embed import EmbedAuthorData

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

        embed.type = data['type']

        embed.title = data.get('title')

        embed.description = data.get('description')

        embed.url = data.get('url')

        embed.color = data.get('color')

        embed.timestamp = data.get('timestamp')  # TODO: Consider how to handle 'timestamp'
        

        # Define a dictionary mapping attribute names to their corresponding classes
        attrs = {
            "author": EmbedAuthor,
            "footer": EmbedFooter,
        }

        # Loop through all the attributes stored in the 'attrs' dictionary
        for attr_name, attr_class in attrs.items():
            # Check if the attribute exists in the data dictionary
            if (attr_data := data.get(attr_name)) is not None:
                # If the attribute name exists in the data payload, create an instance of the attribute class
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
            # it's an embed attribute (eg., author, footer)
            if attr.startswith("_"):
                try:
                    # Fetch the attribute
                    fetched_attr = getattr(self, attr)
                except AttributeError:
                    pass
                else:
                    # Convert the fetched attribute to a dictionary using its to_dict method and adding it to our base dict.
                    base[attr[1:]] = fetched_attr.to_dict()

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
