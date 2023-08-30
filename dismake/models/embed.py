from __future__ import annotations

from typing import TYPE_CHECKING, Any, MutableSequence, Optional, Sequence, Union
from dataclasses import dataclass, field

if TYPE_CHECKING:
    from typing_extensions import Self
    from dismake.types import EmbedData, EmbedType
    from datetime import datetime

__all__: Sequence[str] = ("Embed",)


@dataclass()
class EmbedFooter:
    """Represents an embed footer."""

    text: Optional[str] = field(default=None, repr=True)
    """The footer text, or `None` if not present."""

    icon_url: Optional[str] = field(default=None, repr=True)
    """The URL of the footer icon, or `None` if not present."""


@dataclass()
class EmbedAttachment:
    """Represents an embed attachment."""

    url: Optional[str] = field(default=None, repr=False)
    """The url of the attachment, if present and known, otherwise `None`."""

    height: Optional[int] = field(default=None, repr=False)
    """The height of the attachment, if present and known, otherwise `None`.

    .. note::
        This field cannot be set by bots or webhooks while sending an embed and
        will be ignored during serialization. Expect this to be populated on
        any received embed attached to a message event.
    """

    width: Optional[int] = field(default=None, repr=False)
    """The width of the attachment, if present and known, otherwise `None`.

    .. note::
        This field cannot be set by bots or webhooks while sending an embed and
        will be ignored during serialization. Expect this to be populated on
        any received embed attached to a message event.
    """


@dataclass()
class EmbedProvider:
    """Represents an embed provider.

    .. note::
        This object cannot be set by bots or webhooks while sending an embed and
        will be ignored during serialization. Expect this to be populated on
        any received embed attached to a message event provided by an external
        source.

        **Therefore, you should never need to initialize an instance of this
        class yourself.**
    """

    name: Optional[str] = field(default=None, repr=True)
    """The name of the provider."""

    url: Optional[str] = field(default=None, repr=True)
    """The URL of the provider."""


@dataclass()
class EmbedAuthor:
    """Represents an author of an embed."""

    name: Optional[str] = field(default=None, repr=True)
    """The name of the author, or `None` if not specified."""

    url: Optional[str] = field(default=None, repr=True)
    """The URL that the author's name should act as a hyperlink to.

    This may be `None` if no hyperlink on the author's name is specified.
    """

    icon_url: Optional[str] = field(default=None, repr=False)
    """The author's icon, or `None` if not present."""

    @property
    def is_none(self) -> bool:
        # TODO
        return self.name is None and self.url is None and self.icon_url is None


@dataclass()
class EmbedField:
    """Represents a field in a embed."""

    name: str = field(repr=True)
    """The name of the field."""

    value: str = field(repr=True)
    """The value of the field."""

    inline: Optional[bool] = field(default=False, repr=True)



class Embed:
    """Represents an discord embed."""

    def __init__(
        self,
        *,
        title: Any = None,
        description: Any = None,
        color: Optional[int] = None,  # TODO real color
        type: EmbedType = "rich",
        url: Optional[str] = None,
        timestamp: Optional[Union[datetime, str]] = None,
    ) -> None:
        self.title = title
        self.description = description
        self.color = color
        self.type = type
        self.url = url
        self.timestamp = timestamp

        self._author: EmbedAuthor = EmbedAuthor()
        self._footer: EmbedFooter = EmbedFooter()
        self._image: EmbedAttachment = EmbedAttachment()
        self._thumbnail: EmbedAttachment = EmbedAttachment()
        self._video: EmbedAttachment = EmbedAttachment()
        self._fields: MutableSequence[EmbedField] = list()

    @property
    def author(self) -> EmbedAuthor:
        return self._author

    @property
    def footer(self) -> EmbedFooter:
        return self._footer

    @property
    def image(self) -> EmbedAttachment:
        return self._image

    @property
    def thumbnail(self) -> EmbedAttachment:
        return self._thumbnail

    @property
    def video(self) -> EmbedAttachment:
        return self._video

    @property
    def fields(self) -> MutableSequence[EmbedField]:
        return self._fields

    @classmethod
    def from_dict(cls, data: EmbedData) -> Self:
        embed = cls(
            title=data.get("title"),
            description=data.get("description"),
            color=data.get("color"),
            type=data.get("type") or "rich",
            url=data.get("url"),
            timestamp=data.get("timestamp"),
        )
        if (author := data.get("author")) is not None:
            embed.set_author(
                name=author.get("name"),
                url=author.get("url"),
                icon_url=author.get("icon_url"),
            )

        if (footer := data.get("footer")) is not None:
            embed.set_footer(
                text=footer.get("text"),
                icon_url=data.get("icon_url"),
            )

        if (image := data.get("image")) is not None:
            embed.set_image(
                url=image.get("url"),
                height=image.get("height"),
                width=image.get("width"),
            )

        if (thumbnail := data.get("thumbnail")) is not None:
            embed.set_thumbnail(
                url=thumbnail.get("url"),
                height=thumbnail.get("height"),
                width=thumbnail.get("width"),
            )

        if (video := data.get("video")) is not None:
            embed.set_video(
                url=video.get("url"),
                height=video.get("height"),
                width=video.get("width"),
            )
        
        if (fields := data.get('fields')) is not None:
            for field in fields:
                embed.add_field(name=field['name'], value=field['value'], inline=field.get('inline'))
        return embed

    def set_author(
        self,
        name: Optional[str] = None,
        *,
        icon_url: Optional[str] = None,
        url: Optional[str] = None,
    ) -> Self:
        self._author = EmbedAuthor(name=name, icon_url=icon_url, url=url)
        return self

    def set_footer(
        self, text: Optional[str] = None, icon_url: Optional[str] = None
    ) -> Self:
        self._footer = EmbedFooter(text=text, icon_url=icon_url)
        return self

    def set_image(
        self,
        url: Optional[str] = None,
        height: Optional[int] = None,
        width: Optional[int] = None,
    ) -> Self:
        self._image = EmbedAttachment(url=url, height=height, width=width)
        return self

    def set_thumbnail(
        self,
        url: Optional[str] = None,
        height: Optional[int] = None,
        width: Optional[int] = None,
    ) -> Self:
        self._thumbnail = EmbedAttachment(url=url, height=height, width=width)
        return self

    def set_video(
        self,
        url: Optional[str] = None,
        height: Optional[int] = None,
        width: Optional[int] = None,
    ) -> Self:
        self._video = EmbedAttachment(url=url, height=height, width=width)
        return self

    def add_field(self, name: str, value: str, inline: Optional[bool] = None) -> Self:
        self._fields.append(EmbedField(name=name, value=value, inline=inline))
        return self

    def remove_field(self, index: int) -> Self:
        try:
            del self._fields[index]
        except IndexError:
            pass
        return self

    def insert_field_at(
        self, index: int, name: str, value: str, inline: bool = False
    ) -> Self:
        self._fields.insert(index, EmbedField(name=name, value=value, inline=inline))
        return self

    def to_dict(self) -> EmbedData:
        base: EmbedData = {"type": str(self.type)}
        if self.title:
            base["title"] = str(self.title)

        if self.description is not None:
            base["description"] = str(self.description)

        if self.color is not None:
            base["color"] = int(self.color)

        if self.url is not None:
            base["url"] = self.url

        if self.timestamp is not None:
            base["timestamp"] = str(self.timestamp)

        # if not self.author.is_none:
        #     base['author'] = {'name': self.author.name}
        #     if self.author.icon_url is not None:
        #         base['author']['icon_url'] = self.author.icon_url
        return base
