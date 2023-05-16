from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ..enums import ComponentType
from ..models import PartialEmoji
from .component import Component

if TYPE_CHECKING:
    from ..models import Interaction
    from typing_extensions import Self

__all__ = (
    "SelectOption",
    "StringSelectMenu",
)


class BaseSelect(Component):
    """
    Represents a select menu.

    This class should not be initialized directly.
    All other select menus should subclass this class.

    Parameters
    ----------
    type: :class:`ComponentType`
        The type of the component.
    custom_id: :class:`str`
        The custom ID of the component. If not provided, a random UUID will be generated.
    placeholder: :class:`str`
        The text displayed on the select menu.
    disabled: :str:`bool`
        Indicates whether the component is disabled.
    min_values: :class:`int`
        Determines the minimum number of options that can be selected by the user. (default: 1)
    mxn_values: :class:`int`
        Determines the maximum number of options that can be selected by the user. (default: 1)

    Attributes
    ----------
    view: :class:`View`
        The view associated with the component.
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

    Parameters
    ----------
    label: :class:`str`
        The text displayed on the option.
    value: :class:`str`
        The option's value.
    description: :class:`str`
        The description displayed on the option.
    emoji: :class:`PartialEmoji`
        The emoji displayed on the option
    default: :class:`bool`
        Indicates whether the option is default.
    """

    __slots__ = ("label", "value", "description", "default", "emoji")

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
        self.emoji: PartialEmoji | None
        if emoji is not None:
            if isinstance(emoji, str):
                self.emoji = PartialEmoji.from_str(emoji)
            else:
                self.emoji = emoji
        else:
            self.emoji = None

    def to_dict(self) -> dict[str, Any]:
        """
        Converts a select option into a dict.

        Returns
        -------
        dict[str, Any]
        """
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
    Represents a String select menu.

    Parameters
    ----------
    options: list[:class:`SelectOption`]
        The list of options that will be shown when the user clicks on the menu.
    custom_id: :class:`str`
        The custom ID of the component. If not provided, a random UUID will be generated.
    placeholder: :class:`str`
        The text displayed on the select menu.
    disabled: :str:`bool`
        Indicates whether the component is disabled.
    min_values: :class:`int`
        Determines the minimum number of options that can be selected by the user. (default: 1)
    mxn_values: :class:`int`
        Determines the maximum number of options that can be selected by the user. (default: 1)

    Attributes
    ----------
    view: :class:`View`
        The view associated with the component.
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

    def add_option(self, option: SelectOption) -> Self:
        """
        Append a option to this select menu

        Returns
        -------
        Self
        """
        self.options.append(option)
        return self

    def to_dict(self) -> dict[str, Any]:
        """
        Converts a :class:`StringSelectMenu` into a dict.

        Returns
        -------
        dict[str, Any]
        """
        base = super().to_dict()
        base["options"] = [o.to_dict() for o in self.options]
        return base
