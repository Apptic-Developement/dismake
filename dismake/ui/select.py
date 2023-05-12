from __future__ import annotations

from typing import TYPE_CHECKING, Any

from dismake.models import Interaction
from ..enums import ComponentType
from ..models import PartialEmoji
from .component import Component

if TYPE_CHECKING:
    from ..models import Interaction

__all__ = (
    "SelectOption",
    "StringSelectMenu",
)


class BaseSelect(Component):
    """
    Represents a select menu.

    Attributes
    ----------
    custom_id: :class:`str`
    placeholder: :class:`str`
    min_values: :class:`int`
    max_values: :class:`int`
    disabled: :class:`bool`
    placeholder: :class:`str`
    """

    def __init__(
        self,
        type: ComponentType,
        custom_id: str | None = None,
        placeholder: str | None = None,
        disabled: bool = False,
        min_values: int = 1,
        max_values: int = 1,
    ) -> None:
        super().__init__(type=type, custom_id=custom_id, disabled=disabled)
        self.placeholder = placeholder
        self.min_values = min_values
        self.max_values = max_values

    async def callback(self, interaction: Interaction):
        ...

    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        if self.placeholder is not None:
            base["placeholder"] = self.placeholder
        base.update({"min_value": self.min_values, "max_values": self.max_values})
        if self.disabled is not None:
            base["disabled"] = self.disabled
        return base


class SelectOption:
    """
    Represents a select menu option.

    Attributes
    ----------
    label: :class:`str`
    value: :class:`str`
    description: :class:`str`
    emoji: :class:`PartialEmoji`
    default: :class:`bool`
    """
    __slots__ = (
        "label",
        "value",
        "description",
        "default",
        "emoji"
    )
    def __init__(
        self,
        label: str,
        value: str | None = None,
        description: str | None = None,
        emoji: PartialEmoji | None = None,
        default: bool | None = None,
    ) -> None:
        self.label = label
        self.value = value or label
        self.description = description
        self.default = default
        if emoji is not None:
            if isinstance(emoji, str):
                self.emoji = PartialEmoji.from_str(emoji)
            else:
                self.emoji = emoji
        else:
            self.emoji = None

    def to_dict(self) -> dict[str, Any]:
        base: dict[str, Any] = {
            "label": self.label,
            "value": self.value,
        }
        if self.description is not None:
            base["description"] = self.description
        if self.default is not None:
            base["default"] = self.default
        if self.emoji is not None:
            base["emoji"] = self.emoji.dict(exclude_none=True)
        return base


class StringSelectMenu(BaseSelect):
    """
    Represents a string select menu.

    Attributes
    ----------
    custom_id: :class:`str`
    options: list[:class:`SelectOption`]
    placeholder: :class:`str`
    min_values: :class:`int`
    max_values: :class:`int`
    disabled: :class:`bool`
    """

    def __init__(
        self,
        options: list[SelectOption],
        custom_id: str | None = None,
        placeholder: str | None = None,
        disabled: bool = False,
        min_values: int = 1,
        max_values: int = 1,
    ):
        super().__init__(
            type=ComponentType.STRING_SELECT,
            custom_id=custom_id,
            placeholder=placeholder,
            min_values=min_values,
            max_values=max_values,
            disabled=disabled,
        )
        self.options = options
    def add_option(self, option: SelectOption):
        self.options.append(option)
        return self


    async def callback(self, interaction: Interaction):
        ...

    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base["options"] = [o.to_dict() for o in self.options]
        return base
