from __future__ import annotations

from typing import Optional, Any, Dict, Union
from .component import Component
from ..enums import ButtonStyles, ComponentType
from ..models import PartialEmoji

__all__ = ("Button",)


class Button(Component):
    """
    Represents a discord button.

    Parameters
    ----------
    label: :class:`str`
        The text displayed on the button.
    custom_id: :class:`str`
        A unique identifier for the button.
    style: :class:`ButtonStyles`
        The style of the button
    emoji: Union[:class:`Emoji`, :class:`str`]
        The emoji displayed on the button.
    url: :class:`str`
        If set, this button will act as a link to the given URL.
    disabled: :class:`bool`
        If True, the button will be disabled and cannot be clicked.
    
    Attributes
    ----------
    view: :class:`View`
        The view associated with the component.
    """
    def __init__(
        self,
        label: Optional[str],
        custom_id: Optional[str],
        style: Optional[ButtonStyles],
        emoji: Optional[Union[PartialEmoji, str]] = None,
        url: Optional[str] = None,
        disabled: Optional[bool] = None,
    ) -> None:
        self.type = ComponentType.BUTTON
        super().__init__(type=self.type, custom_id=custom_id, disabled=disabled)
        self.label = label
        self.style = style or ButtonStyles.PRIMARY
        self.url = url
        self.emoji: Optional[PartialEmoji]
        if emoji:
            if isinstance(emoji, PartialEmoji):
                self.emoji = emoji
            else:
                self.emoji = PartialEmoji.from_str(emoji)
        else:
            self.emoji = None

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the button into dict.

        Returns
        -------
        dict[str, Any]
        """
        base = super().to_dict()
        if not self.url:
            base["label"] = self.label
            base["style"] = self.style.value
            if self.emoji is not None:
                base["emoji"] = self.emoji.dict(exclude_none=True)
        else:
            base["label"] = self.label
            base["style"] = ButtonStyles.LINK.value
            base["url"] = self.url
            if self.emoji is not None:
                base["emoji"] = self.emoji.dict(exclude_none=True)
            if base.get("custom_id"):
                base.pop("custom_id")

        return base
