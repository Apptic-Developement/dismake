from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Sequence, Union

if TYPE_CHECKING:
    from ..enums import Locale, ChannelType, ApplicationCommandOptionType

__all__: Sequence[str] = ("Option", "Parameter", "P")


class Choice:
    def __init__(
        self,
        name: str,
        name_localizations: Optional[Dict[Locale, str]] = None,
        value: Optional[Union[str, int]] = None,
    ) -> None:
        self.name = name
        self.name_localizations = name_localizations
        self.value = value or name

    def to_dict(self) -> Dict[str, Any]:
        base: Dict[str, Any] = {"name": self.name, "value": self.value}
        if self.name_localizations is not None:
            base["name_localizations"] = {
                k.value: v for k, v in self.name_localizations.items()
            }
        return base


class Option:
    def __init__(
        self,
        name: str,
        description: str,
        required: Optional[bool] = None,
        choices: Optional[List[Choice]] = None,
        name_localizations: Optional[Dict[Locale, str]] = None,
        description_localizations: Optional[Dict[Locale, str]] = None,
        channel_types: Optional[List[ChannelType]] = None,
        min_value: Optional[int] = None,
        max_value: Optional[int] = None,
        autocomplete: Optional[bool] = None,
    ) -> None:
        self.name = name
        self.description = description
        self.required = required
        self.choices = choices
        self.name_localizations = name_localizations
        self.description_localizations = description_localizations
        self.channel_types = channel_types
        self.min_value = min_value
        self.max_value = max_value
        self.autocomplete = autocomplete
        self.type: ApplicationCommandOptionType

    def to_dict(self) -> Dict[str, Any]:
        base: Dict[str, Any] = {
            "type": self.type.value,
            "name": self.name,
            "description": self.description,
        }

        if self.required is not None:
            base["required"] = self.required
        if self.choices is not None:
            base["choices"] = self.choices
        if self.name_localizations is not None:
            base["name_localizations"] = {
                k.value: v for k, v in self.name_localizations.items()
            }
        if self.description_localizations is not None:
            base["description_localizations"] = {
                k.value: v for k, v in self.description_localizations.items()
            }
        if self.channel_types is not None:
            base["channel_types"] = self.channel_types

        if self.min_value is not None:
            key = (
                "min_value"
                if self.type == ApplicationCommandOptionType.INTEGER
                else "min_length"
            )
            base[key] = self.min_value
        if self.max_value is not None:
            key = (
                "max_value"
                if self.type == ApplicationCommandOptionType.INTEGER
                else "max_length"
            )
            base[key] = self.max_value

        if self.autocomplete is not None:
            base["autocomplete"] = self.autocomplete

        return base


def Parameter(*args: Any, **kwargs: Any) -> Any:
    return Option(*args, **kwargs)


P = Parameter
