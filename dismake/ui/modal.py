from __future__ import annotations


from ..enums import ComponentType, TextInputStyle
from .component import Component
from .view import View


class Modal(View):
    def __init__(self, title: str) -> None:
        super().__init__()


class TextInput(Component):
    def __init__(
        self,
        label: str,
        type: ComponentType,
        custom_id: str | None,
        disabled: bool | None,
        style: TextInputStyle = TextInputStyle.short,
        min_length: int | None = None,
        max_length: int | None = None,
        required: bool | None = None,
        value: str | None = None,
        placeholder: str | None = None,
    ) -> None:
        super().__init__(type, custom_id, disabled)
        self.label = label
        self.style = style
        self.min_length = min_length
        self.max_length = max_length
        self.required = required
        self.value = value
        self.placeholder = placeholder
    
                

