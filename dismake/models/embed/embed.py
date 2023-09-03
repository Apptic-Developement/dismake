from __future__ import annotations


from typing import (
    TYPE_CHECKING,
    Any,
    List,
    Optional,
    Sequence,
    Tuple,
)


from .proxys import EmbedAuthor, EmbedField, EmbedFooter, EmbedAttachment, EmbedProvider
from datetime import datetime, timezone
from ...utils import parse_time
from ..color import Color

if TYPE_CHECKING:
    from typing_extensions import Self
    from ...types import EmbedData, EmbedType, EmbedFieldData


__all__: Sequence[str] = ("Embed",)


class Embed:
    """Represents a Discord embed.

    For your convenience, this class implicitly casts parameters that expect a string to str.

    Attributes
    -----------
    title: str
        The title of the embed. Can be up to 256 characters.
    type: str
        The type of embed. Usually "rich".
    description: str
        The description of the embed. Can be up to 4096 characters.
    url: str
        The URL of the embed.
    timestamp: Optional[datetime]
        The timestamp of the embed content, an aware datetime.
        If a naive datetime is passed, it's converted to an aware datetime with the local timezone.
    color: Color
        The color code of the embed.
    """

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
        "_image",
        "_thumbnail",
        "_video",
        "_provider",
    )

    def __init__(
        self,
        *,
        title: Any = None,
        description: Any = None,
        type: EmbedType = "rich",
        url: Any = None,
        timestamp: Optional[datetime] = None,
        color: Optional[Color] = None,
    ) -> None:
        self.title = title
        self.description = description
        self.type = type
        self.url = url
        self.color = color
        self.timestamp: Optional[datetime]
        if isinstance(timestamp, datetime):
            if timestamp.tzinfo is None:
                self.timestamp = timestamp.astimezone()
        elif timestamp is None:
            self.timestamp = None
        else:
            raise TypeError(
                f"Expected datetime.datetime or None received {timestamp.__class__.__name__} instead"
            )

    @classmethod
    def from_dict(cls, data: EmbedData) -> Self:
        """Converts a dictionary into an Embed object, provided the data is in the
        format expected by Discord.

        Parameters
        -----------
        data: EmbedData
            The dictionary containing the data to convert into an Embed.

        Returns
        --------
        Embed
            An Embed object created from the provided dictionary.
        """
        embed = cls.__new__(cls)

        (embed.title, embed.description, embed.type, embed.url) = (
            data.get("title"),
            data.get("description"),
            data["type"],
            data.get("url"),
        )

        try:
            embed.timestamp = parse_time(data["timestamp"])
        except KeyError:
            pass

        try:
            embed.color = Color(data["color"])
        except KeyError:
            pass

        if (author_data := data.get("author")) is not None:
            setattr(embed, "_author", EmbedAuthor.from_dict(author_data))

        if (footer_data := data.get("footer")) is not None:
            setattr(embed, "_footer", EmbedFooter.from_dict(footer_data))

        if (image_data := data.get("image")) is not None:
            setattr(embed, "_image", EmbedAttachment.from_dict(image_data))

        if (thumbnail_data := data.get("thumbnail")) is not None:
            setattr(embed, "_thumbnail", EmbedAttachment.from_dict(thumbnail_data))

        if (video_data := data.get("video")) is not None:
            setattr(embed, "_video", EmbedAttachment.from_dict(video_data))

        if (provider_data := data.get("provider")) is not None:
            setattr(embed, "_provider", EmbedProvider.from_dict(provider_data))
        if (fields_data := data.get("fields")) is not None:
            temp_fields: List[EmbedField] = list()
            for field_data in fields_data:
                temp_fields.append(EmbedField.from_dict(field_data))

            embed._fields = temp_fields
        return embed

    def to_dict(self) -> EmbedData:
        """Converts this embed object into a dict."""

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
            base["color"] = self.color.value

        if self.timestamp is not None:
            if self.timestamp.tzinfo:
                base["timestamp"] = self.timestamp.astimezone(
                    tz=timezone.utc
                ).isoformat()
            else:
                base["timestamp"] = self.timestamp.replace(
                    tzinfo=timezone.utc
                ).isoformat()

        if self.url is not None:
            base["url"] = self.url

        return base

    def __str__(self) -> str:
        """Returns a string representation of the Embed object."""
        return f"Embed(title='{self.title}', color='{self.color}', fields='{10}')"

    def copy(self) -> Self:
        """Returns a shallow copy of the embed."""
        return self.from_dict(self.to_dict())

    def __len__(self) -> int:
        attrs = (
            len(attr)
            for attr in (
                self.title,
                self.description,
                self.author.name,
                self.footer.text,
            )
            if attr is not None
        )
        fields = (
            (len(field.name) + len(field.value))
            for field in self.fields
            if field.name and field.value
        )
        return sum(attrs) + sum(fields)

    @property
    def author(self) -> EmbedAuthor:
        """Returns an ``EmbedAuthor`` representing the author of the embed.

        If the attribute has no value, an empty ``EmbedAuthor`` will be returned.
        """
        return getattr(self, "_author", EmbedAuthor())

    def set_author(
        self,
        name: Optional[str] = None,
        *,
        url: Optional[str] = None,
        icon_url: Optional[str] = None,
    ) -> Self:
        """Sets the author for the embed content.

        This method returns the class instance to allow for fluent-style chaining.

        Parameters
        -----------
        name: Optional[str]
            The name of the author. Can be up to 256 characters.
        url: Optional[str]
            The URL for the author.
        icon_url: Optional[str]
            The URL of the author's icon. Only HTTP(S) URLs are supported.
            Inline attachment URLs are also supported.

        Note
        ----
        If all parameters are set to ``None``, the author information in the embed
        will be cleared.
        """
        if name is None:
            self._author = None
        else:
            self._author = EmbedAuthor(name=name, url=url, icon_url=icon_url)
        return self

    @property
    def footer(self) -> EmbedFooter:
        """Returns an ``EmbedFooter`` denoting the footer contents.

        If the attribute has no value, an empty ``EmbedFooter`` will be returned.
        """
        return getattr(self, "_footer", EmbedFooter())

    def set_footer(
        self,
        text: Optional[str] = None,
        *,
        icon_url: Optional[str] = None,
    ) -> Self:
        """Sets the footer for the embed content.

        This method returns the class instance to allow for fluent-style chaining.

        Parameters
        -----------
        text: str
            The footer text. Can only be up to 2048 characters.
        icon_url: str
            The URL of the footer icon. Only HTTP(S) is supported.
            Inline attachment URLs are also supported.

        Note
        ----
        If all parameters are set to ``None``, the footer information in the embed
        will be cleared.
        """
        if text is None:
            self._footer = None

        else:
            self._footer = EmbedFooter(text=text, icon_url=icon_url)
        return self

    @property
    def fields(self) -> List[EmbedField]:
        """List[``EmbedField``]: Returns a `list` of ``EmbedProxy`` denoting the field contents.

        If the attribute has no value, an empty list will be returned.
        """
        return getattr(self, "_fields", [])

    def add_field(self, name: str, value: str, inline: Optional[bool] = None) -> Self:
        """Adds a field to the embed object.

        This function returns the class instance to allow for fluent-style
        chaining. Can only be up to 25 fields.

        Parameters
        -----------
        name: str
            The name of the field. Can only be up to 256 characters.
        value: str
            The value of the field. Can only be up to 1024 characters.
        inline: Optional[bool]
            Whether the field should be displayed inline.
        """
        if not getattr(self, "_fields", None):
            self._fields: List[EmbedField] = []

        self.fields.append(EmbedField(name=name, value=value, inline=inline))
        return self

    @property
    def image(self) -> EmbedAttachment:
        """Returns an ``EmbedAttachment`` representing the image of the embed.

        If the attribute has no value, an empty ``EmbedAttachment`` will be returned.
        """
        return getattr(self, "_image", EmbedAttachment())

    def set_image(
        self,
        url: Optional[str] = None,
    ) -> Self:
        """Sets the image for the embed content.

        This method returns the class instance to allow for fluent-style chaining.

        Parameters
        -----------
        url: Optional[str]
            The URL of the image.

        Note
        ----
        If all parameters are set to ``None``, the image information in the embed
        will be cleared.
        """
        if url is None:
            self._image = None

        self._image = EmbedAttachment(url=url)
        return self

    @property
    def thumbnail(self) -> EmbedAttachment:
        """Returns an ``EmbedAttachment`` representing the thumbnail image of the embed.

        If the attribute has no value, an empty ``EmbedAttachment`` will be returned.
        """
        return getattr(self, "_thumbnail", EmbedAttachment())

    def set_thumbnail(self, url: Optional[str] = None) -> Self:
        """Sets the thumbnail image for the embed content.

        This method returns the class instance to allow for fluent-style chaining.

        Parameters
        -----------
        url: Optional[str]
            The URL of the thumbnail image.

        Note
        ----
        If all parameters are set to ``None``, the thumbnail image information in the embed
        will be cleared.
        """
        if url is None:
            self._thumbnail = None

        self._thumbnail = EmbedAttachment(url=url)
        return self

    @property
    def video(self) -> EmbedAttachment:
        """Returns an ``EmbedVideo`` representing the video attachment of the embed.

        If the attribute has no value, an empty ``EmbedVideo`` will be returned.
        """
        return getattr(self, "_video", EmbedAttachment())

    @property
    def provider(self) -> EmbedProvider:
        """Returns an ``EmbedProvider`` representing the provider of the embed.

        If the attribute has no value, an empty ``EmbedProvider`` will be returned.
        """
        return getattr(self, "_provider", EmbedProvider())
