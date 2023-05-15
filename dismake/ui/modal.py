from __future__ import annotations
import uuid

from typing import Any, TYPE_CHECKING

from dismake.types import AsyncFunction

from ..enums import ComponentType, TextInputStyle
from .component import Component
from .view import Row

if TYPE_CHECKING:
    from typing_extensions import Self
__all__ = ("Modal", "TextInput")


class Modal:
    def __init__(self, title: str, custom_id: str | None = None) -> None:
        self.components: list[Row] = list()
        self.title = title
        self.custom_id = custom_id or str(uuid.uuid4())
        self.on_submit: AsyncFunction

    def __repr__(self) -> str:
        return f"<Modal components={len(self.components)!r}>"

    def add_item(self, item: TextInput) -> Self:
        self.components.append(Row().add_component(item))
        return self

    def to_dict(self) -> dict[str, Any]:
        base = {
            "title": self.title,
            "custom_id": self.custom_id,
            "components": [r.to_dict() for r in self.components],
        }
        return base


class TextInput(Component):
    def __init__(
        self,
        label: str,
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
