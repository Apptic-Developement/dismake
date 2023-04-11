from __future__ import annotations

import uuid
from typing import Optional, Any, Dict
from .component import Component
from ..enums import ButtonStyles, ComponentTypes

__all__ = ("Button",)


class Button(Component):
    def __init__(
        self,
        label: str,
        custom_id: Optional[str],
        style: Optional[ButtonStyles],
        emoji: Optional[Any] = None,
        url: Optional[str] = None,
        disabled: Optional[bool] = None
    ) -> None:
        self.type = ComponentTypes.BUTTON
        super().__init__(type=self.type, custom_id=custom_id, disabled=disabled)
        self.label = label
        self.style = style or ButtonStyles.PRIMARY
        self.emoji = emoji
        self.url = url

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        if not self.url:
            base["label"] = self.label
            base["style"] = self.style.value
        else:
            base["label"] = self.label
            base["style"] = ButtonStyles.LINK.value
            base["url"] = self.url
            if base.get("custom_id"):
                base.pop("custom_id")

        return base
