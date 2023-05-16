from __future__ import annotations

import uuid

from typing import Any, TYPE_CHECKING
from ..enums import ComponentType, TextInputStyle
from .component import Component
from .view import View

if TYPE_CHECKING:
    from ..models import Interaction
    from ..types import AsyncFunction


__all__ = ("Modal", "TextInput")




class Modal(View):
    def __init__(self, title: str, custom_id: str | None = None) -> None:
        super().__init__()
        self.title = title
        self.custom_id = custom_id or str(uuid.uuid4())
        self.values: list[str] = list()
        self.callback: AsyncFunction = self.on_submit

    async def on_submit(self, interaction: Interaction):
        ...
    def __repr__(self) -> str:
        return f"<Modal title={self.title!r}>"

    def to_dict(self) -> dict[str, Any]:
        base = {
            "title": self.title,
            "custom_id": self.custom_id,
            "components": super().to_dict()
        }
        return base


class TextInput(Component):
    def __init__(
        self,
        label: str | None = None,
        style: TextInputStyle = TextInputStyle.short,
        placeholder: str | None = None,
        custom_id: str | None = None,
        disabled: bool | None = None,
        min_length: int | None = None,
        max_length: int | None = None,
        required: bool | None = None,
        value: str | None = None,
    ) -> None:
        super().__init__(ComponentType.TEXT_INPUT, custom_id, disabled)
        self.label = label
        self.style = style
        self.min_length = min_length
        self.max_length = max_length
        self.required = required
        self.value = value
        self.placeholder = placeholder

    def __repr__(self) -> str:
        return (
            f"<TextInput label={self.label!r}>"
        )

    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({"label": self.label, "style": self.style.value})
        if self.min_length is not None:
            base["min_length"] = self.min_length
        if self.max_length is not None:
            base["max_length"] = self.max_length
        if self.required is not None:
            base["required"] = self.required
        if self.value is not None:
            base["value"] = self.value
        if self.placeholder is not None:
            base["placeholder"] = self.placeholder
        return base
