from __future__ import annotations

import typing
import attrs

if typing.TYPE_CHECKING:
    from typing_extensions import TypeAlias, Self
    from dismake.types import EmbedData
    from datetime import datetime

__all__: typing.Sequence[str] = ("Embed",)


EmbedType: TypeAlias = typing.Literal[
    "rich", "image", "video", "gifv", "article", "link"
]


@attrs.define(hash=False, kw_only=True, weakref_slot=False)
class EmbedFooter:
    """Represents an embed footer."""

    # Discord says this is never None. We know that is invalid because Discord.py
    # sets it to None. Seems like undocumented behaviour again.
    text: typing.Optional[str] = attrs.field(default=None, repr=True)
    """The footer text, or `None` if not present."""

    icon_url: typing.Optional[str] = attrs.field(default=None, repr=True)
    """The URL of the footer icon, or `None` if not present."""


@attrs.define(hash=False, kw_only=True, weakref_slot=False)
class EmbedAttachment:
    """Represents an embed attachment."""

    url: typing.Optional[str] = attrs.field(default=None, repr=False)
    """The url of the attachment, if present and known, otherwise `None`."""

    height: typing.Optional[int] = attrs.field(default=None, repr=False)
    """The height of the attachment, if present and known, otherwise `None`.

    .. note::
        This field cannot be set by bots or webhooks while sending an embed and
        will be ignored during serialization. Expect this to be populated on
        any received embed attached to a message event.
    """

    width: typing.Optional[int] = attrs.field(default=None, repr=False)
    """The width of the attachment, if present and known, otherwise `None`.

    .. note::
        This field cannot be set by bots or webhooks while sending an embed and
        will be ignored during serialization. Expect this to be populated on
        any received embed attached to a message event.
    """


@attrs.define(hash=False, kw_only=True, weakref_slot=False)
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

    name: typing.Optional[str] = attrs.field(default=None, repr=True)
    """The name of the provider."""

    url: typing.Optional[str] = attrs.field(default=None, repr=True)
    """The URL of the provider."""


@attrs.define(hash=False, kw_only=True, weakref_slot=False)
class EmbedAuthor:
    """Represents an author of an embed."""

    name: typing.Optional[str] = attrs.field(default=None, repr=True)
    """The name of the author, or `None` if not specified."""

    url: typing.Optional[str] = attrs.field(default=None, repr=True)
    """The URL that the author's name should act as a hyperlink to.

    This may be `None` if no hyperlink on the author's name is specified.
    """

    icon_url: typing.Optional[str] = attrs.field(default=None, repr=False)
    """The author's icon, or `None` if not present."""

    @property
    def is_none(self) -> bool:
        # TODO
        return self.name is None and self.url is None and self.icon_url is None


@attrs.define(hash=False, kw_only=True, weakref_slot=False)
class EmbedField:
    """Represents a field in a embed."""

    name: str = attrs.field(repr=True)
    """The name of the field."""

    value: str = attrs.field(repr=True)
    """The value of the field."""

    _inline: bool = attrs.field(alias="inline", default=False, repr=True)

    # Use a property since we then keep the consistency of not using `is_`
    # in the constructor for `_inline`.
    @property
    def is_inline(self) -> bool:
        """Return `True` if the field should display inline.

        Defaults to `False`.
        """
        return self._inline

    @is_inline.setter
    def is_inline(self, value: bool) -> None:
        self._inline = value


class Embed:
    """Represents an discord embed."""

    def __init__(
        self,
        *,
        title: typing.Any = None,
        description: typing.Any = None,
        color: typing.Optional[int] = None, # TODO real color
        type: EmbedType = "rich",
        url: typing.Optional[str] = None,
        timestamp: typing.Optional[datetime] = None,
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
        self._fields: typing.MutableSequence[EmbedField] = list()

    @classmethod
    def from_dict(cls, data: EmbedData) -> Self:
        raise NotImplementedError

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
    def fields(self) -> typing.MutableSequence[EmbedField]:
        return self._fields

    def set_author(
        self,
        name: typing.Optional[str] = None,
        *,
        icon_url: typing.Optional[str] = None,
        url: typing.Optional[str] = None,
    ) -> Self:
        self._author = EmbedAuthor(name=name, icon_url=icon_url, url=url)
        return self

    def set_footer(
        self, text: typing.Optional[str] = None, icon_url: typing.Optional[str] = None
    ) -> Self:
        self._footer = EmbedFooter(text=text, icon_url=icon_url)
        return self

    def set_image(
        self,
        url: typing.Optional[str] = None,
        height: typing.Optional[int] = None,
        width: typing.Optional[int] = None,
    ) -> Self:
        self._image = EmbedAttachment(url=url, height=height, width=width)
        return self

    def set_thumbnail(
        self,
        url: typing.Optional[str] = None,
        height: typing.Optional[int] = None,
        width: typing.Optional[int] = None,
    ) -> Self:
        self._thumbnail = EmbedAttachment(url=url, height=height, width=width)
        return self

    def set_video(
        self,
        url: typing.Optional[str] = None,
        height: typing.Optional[int] = None,
        width: typing.Optional[int] = None,
    ) -> Self:
        self._video = EmbedAttachment(url=url, height=height, width=width)
        return self

    def add_field(self, name: str, value: str, inline: bool = False) -> Self:
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
        base: EmbedData = {"type": self.type}
        if self.title:
            base['title'] = str(self.title)
        
        if self.description is not None:
            base['description'] = str(self.description)
        
        if self.color is not None:
            base['color'] = int(self.color)
        
        if self.url is not None:
            base['url'] = self.url
        
        if self.timestamp is not None:
            base['timestamp'] = str(self.timestamp)
        
        # if not self.author.is_none:
        #     base['author'] = {'name': self.author.name}
        #     if self.author.icon_url is not None:
        #         base['author']['icon_url'] = self.author.icon_url
        return base
