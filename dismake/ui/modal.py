from __future__ import annotations

import uuid, inspect
from typing import Annotated, Any, TYPE_CHECKING, Callable, get_origin

from functools import wraps
from ..enums import ComponentType, TextInputStyle
from .component import Component
from .view import Row
from ..errors import ModalException


if TYPE_CHECKING:
    from typing_extensions import Self
    from ..models import Interaction
    from ..types import AsyncFunction


__all__ = ("Modal", "TextInput")


def _get_text_inputs(coro: AsyncFunction) -> list[TextInput]:
    inputs: list[TextInput] = list()
    parameters = inspect.signature(coro).parameters
    for k, v in parameters.items():
        # k: name of the parameter
        # v: Annotation of the parameter
        annotation: Annotated = v.annotation
        if get_origin(annotation) == Annotated:
            text_input: TextInput = annotation.__metadata__[0]
            input_type: type = annotation.__args__[0]
            if input_type not in (str, int, float, bool):
                raise ValueError(
                    f"Text input can only support 'str, int, float, bool' types not {input_type.__name__!r}"
                )
            text_input.type = input_type
            if text_input.label is None:
                text_input.label = k
            inputs.append(text_input)
    return inputs


class Modal:
    def __init__(self, title: str, custom_id: str | None = None) -> None:
        self.components: list[Row] = list()
        self.title = title
        self.custom_id = custom_id or str(uuid.uuid4())
        self.callback: AsyncFunction | None = None

    async def _invoke(self, interaction: Interaction):
        ...

    def on_submit(self, coro: AsyncFunction) -> Self:
        @wraps(coro)
        def wrapper(*_, **__) -> Self:
            inputs = _get_text_inputs(coro)
            if not inputs:
                raise ModalException(
                    f"{self.title!r} modal's callback does not have any text input."
                )
            for input in inputs:
                self.components.append(Row().add_component(input))
            self.callback = coro
            return self

        return wrapper()

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
        label: str | None = None,
        style: TextInputStyle = TextInputStyle.short,
        type: type = str,  # str | int | bool | float
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
        self.type = type

    def __repr__(self) -> str:
        return (
            f"<TextInput label={self.label!r} value_type={self.type.__name__!r}>"
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
