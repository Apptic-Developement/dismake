from __future__ import annotations
from typing import Any, Optional, Union

from pydantic import BaseModel, validator
from ..enums import ComponentType
from .emoji import PartialEmoji

__all__ = ("SelectOption", "Component", "ActionRow", "TextInput")


class Component(BaseModel):
    type: ComponentType
    custom_id: Optional[str] = None


class ActionRow(Component):
    type: ComponentType = ComponentType.ACTION_ROW
    components: list[Component] = list()

    @validator("components")
    def _validate_components(cls, value: list[Component]) -> list[Component]:
        if len(value) > 5:
            raise ValueError("An action row can only have 5 components.")
        if ComponentType.ACTION_ROW in [t.type for t in value]:
            raise ValueError("A action row can not have another action row.")

        if (
            ComponentType.STRING_SELECT
            or ComponentType.ROLE_SELECT
            or ComponentType.CHANNEL_SELECT
            or ComponentType.MENTIONABLE_SELECT
            and ComponentType.BUTTON in ([t.type for t in value])
        ):
            raise ValueError(
                "An action row can not contains select option and button option option together."
            )

        return value

    @property
    def is_full(self) -> bool:
        return len(self.components) == 5


class SelectOption(BaseModel):
    label: str
    value: str
    description: Optional[str]
    emoji: Optional[Union[PartialEmoji, dict[str, Any], str]]
    default: Optional[bool]


class TextInput(Component):
    value: Optional[str]
