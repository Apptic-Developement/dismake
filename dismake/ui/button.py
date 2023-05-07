from __future__ import annotations

from typing import Optional, Any, Dict, Union
from .component import Component
from ..enums import ButtonStyles, ComponentTypes
from ..models import PartialEmoji
__all__ = ("Button",)


class Button(Component):
    def __init__(
        self,
        label: str,
        custom_id: Optional[str],
        style: Optional[ButtonStyles],
        emoji: Optional[Union[PartialEmoji, str]] = None,
        url: Optional[str] = None,
        disabled: Optional[bool] = None,
    ) -> None:
        self.type = ComponentTypes.BUTTON
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
