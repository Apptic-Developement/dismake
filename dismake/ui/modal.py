from __future__ import annotations

import uuid

from typing import Any, TYPE_CHECKING
from ..enums import ComponentType, TextInputStyle
from .component import Component
from ..models import ModalSubmitData

if TYPE_CHECKING:
    from ..models import Interaction
    from typing_extensions import Self


__all__ = ("Modal", "TextInput")


class Modal:
    """
    Represents a UI Modal dialog.

    Parameters
    ----------
    title: :class:`str`
        The title of the modal.
        Must be 45 characters or fewer.
    custom_id: :class:`str`
        The custom ID of the modal. If not provided, a random UUID will be generated.
        Must be 100 characters or fewer.

    Attributes
    ----------
    children: :class:`list[TextInput]`
        A list of :class:`TextInput` components.
    """

    def __init__(self, title: str, custom_id: str | None = None) -> None:
        self._title = title
        self._custom_id = custom_id or str(uuid.uuid4())
        self._children: list[TextInput] = list()

        if len(title) > 45:
            raise ValueError("Modal title must be 45 characters or fewer.")

        if len(self._custom_id) > 100:
            raise ValueError("Modal custom_id must be 100 characters or fewer.")

        if len(self.children) > 5:
            raise ValueError("Modal cannot have more than 5 children.")

    def add_item(self, item: TextInput) -> Self:
        self._children.append(item)
        return self

    @property
    def title(self) -> str:
        return self._title

    @property
    def custom_id(self) -> str:
        return self._custom_id

    @property
    def children(self) -> list[TextInput]:
        return self._children

    async def on_error(self, interaction: Interaction, exception: Exception) -> Any:
        pass

    async def _invoke(self, interaction: Interaction) -> Any:
        assert isinstance(
            interaction.data, ModalSubmitData
        ), "Invalid interaction recived."
        inputs = [t for r in interaction.data.components for t in r.components]
        for input in inputs:
            item = list(
                filter(lambda x: x.custom_id == input.custom_id, self.children)
            )[0]
            if not item:
                return await self.on_error(
                    interaction,
                    Exception(
                        f"Modal interaction referencing unknown item custom_id {input.custom_id!r}. Discarding"
                    ),
                )
            item.value = input.value
        try:
            await self.on_submit(interaction)
        except Exception as e:
            await self.on_error(interaction, e)

    async def on_submit(self, interaction: Interaction) -> Any:
        pass

    def __repr__(self) -> str:
        return f"<Modal title={self.title!r}>"

    def to_dict(self) -> dict[str, Any]:
        """
        Converts a :class:`Modal` into a dict.

        Returns
        -------
        dict[str, Any]
        """
        base = {
            "title": self.title,
            "custom_id": self.custom_id,
            "components": [
                {"type": ComponentType.ACTION_ROW.value, "components": [t.to_dict()]}
                for t in self.children[:5]
            ],
        }
        return base


class TextInput(Component):
    """
    Represents a text input component.

    Parameters
    ----------
    label: :class:`str`
        The text displayed to the top of the text field.
        Must be 45 characters or fewer.
    style: :class:`TextInputStyle`
        The style of the text field.
    placeholder: :class:`str`
        The placeholder text displayed when the text field is empty.
        Must be 100 characters or fewer.
    custom_id: :class:`str`
        The custom ID of the text input. If not provided, a random UUID will be generated.
    disabled: :class:`bool`
        Whether the text field is disabled.
    min_length: :class:`int`
        The minimum number of characters that must be entered.
        Defaults to 0 and must be less than 4000.
    max_length: :class:`int`
        The maximum number of characters that can be entered.
        Must be between 1 and 4000.
    required: :class:`bool`
        Whether the text field is required.
    value: :class:`str`
        Pre-fills the input text field with this value.
        Must be 4000 characters or fewer.
    """

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
        if len(self.label) > 45:
            raise ValueError("Label must be 45 characters or fewer.")
        if self.value is not None and len(self.value) > 4000:
            raise ValueError("Value must be 4000 characters or fewer.")

        if self.min_length is not None and self.max_length is not None:
            if self.min_length > self.max_length:
                raise ValueError("Min length must be less than max length.")

        if self.min_length is not None:
            if self.min_length < 1:
                raise ValueError("Min length must be greater than 0.")
        if self.max_length is not None:
            if self.max_length < 1:
                raise ValueError("Max length must be greater than 0.")

    def __repr__(self) -> str:
        return f"<TextInput label={self.label!r}>"

    def to_dict(self) -> dict[str, Any]:
        """
        Converts a :class:`TextInput` to a dict.

        Returns
        -------
        dict[str, Any]
        """
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
