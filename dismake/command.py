from __future__ import annotations

from typing import Any, Optional
from inspect import signature
from functools import wraps
from dismake.types.command import OptionType
from .types import AsyncFunction, CommandTypes

__all__ = ("SlashCommand", "Option", "Choice")


async def _default_slash_command_callback(*args, **kwargs):
    # TODO: Response 
    pass


class Choice:
    def __init__(
        self,
        name: str ,
        value: str | int | float,
        name_localizations: list[dict] | None = None
    ) -> None:
        self._name = name
        self._value = value
        self._name_localizations = name_localizations


    def _to_dict(self) -> dict[str, Any]:
        return {
            'name': self._name,
            'value': self._value,
            'name_localizations': self._name_localizations,
        }

# class SlashOption(BaseModel):
#     type: int
#     name: str
#     description: str
#     name_localizations: Optional[dict[str, str]] = None
#     description_localizations: Optional[dict[str, str]] = None
#     required: Optional[bool] = False
#     choices: Optional[list[Choice]] = None
#     options: list[SlashOption] = list()
#     channel_types: Optional[list[str]] = None
#     min_value: Optional[float] = None
#     max_value: Optional[float] = None
#     min_length: Optional[int] = None
#     max_length: Optional[int] = None
#     autocomplete: Optional[bool] = None
#     autocomplete_callback: Optional[AsyncFunction] = None
#     callback: Optional[AsyncFunction] = None

class Option:
    _level: int = 1
    def __init__(
        self,
        name: str,
        description: str,
        type: int = OptionType.STRING,
        required: bool = False,
        autocomplete: bool = False,
        autocompleter: Optional[AsyncFunction] = None,
        choices: list[Choice] | None= None,
        min_value: int | None = None,
        max_value: int | None = None,
        channel_types: int | None = None,
        options: list[Option] | None = None 
    ) -> None:
        self._name = name
        self._description = description
        self._type = type
        self._required = required
        self._autocomplete = autocomplete
        self._autocompleter = autocompleter
        self._choices = choices
        self._min_value = min_value
        self._max_value = max_value
        self._channel_types = channel_types
        self._options = options

        self._callback: AsyncFunction = _default_slash_command_callback


    def __str__(self) -> str:
        return f"<dismake.Option name='{self._name}'>"
    @property
    def callback(self) -> Optional[AsyncFunction]:
        return self._callback

    @callback.setter
    def callback(self, value: AsyncFunction | None):
        if value is None:
            self._callback = _default_slash_command_callback
            return
        self._callback = value

    def to_dict(self) -> dict:
        _as_dict = {
            "name": self._name,
            "description": self._description,
            "type": self._type,
            "required": self._required,
            "autocomplete": self._autocomplete
        }
        if self._choices:
            _as_choices = []
            for choice in self._choices:
                _as_choices.append(
                    {"name": choice._name, "value": choice._value}
                )
            _as_dict["choices"] = _as_choices

        return _as_dict
        


class SlashCommand:
    _level: int = 1
    def __init__(
        self,
        name: str,
        description: Optional[str],
        application_id: Optional[int] = None,
        guild_id: Optional[int] = None,
        name_localizations: Optional[dict[str, str]] = None,
        description_localizations: Optional[dict[str, str]] = None,
        default_member_permissions: Optional[str] = None,
        dm_permission: Optional[bool] = True,
        default_permission: Optional[bool] = True,
        nsfw: Optional[bool] = False,
        version: Optional[int] = 1,
    ) -> None:
        self._name = name
        self._description = description or "No description provided."
        self._type = CommandTypes.SLASH
        self._application_id = application_id
        self._guild_id = guild_id
        self._name_localizations = name_localizations
        self._description_localizations = description_localizations
        self._options: list[Option] = list()
        self._default_member_permissions = default_member_permissions
        self._dm_permission = dm_permission
        self._default_permission = default_permission
        self._nsfw = nsfw
        self._version = version
        self._options = []
        self._subcommands = []
        self._callback: AsyncFunction = _default_slash_command_callback

    def __str__(self) -> str:
        return f"<Command name='{self._name}' description='{self._description}'>"

    @property
    def callback(self) -> AsyncFunction:
        return self._callback
    
    @callback.setter
    def callback(self, value: AsyncFunction | None):
        if value is None:
            self._callback = _default_slash_command_callback
            return
        self._callback = value

    def to_dict(self) -> dict:
        _as_dict = {
            "name": self._name,
            "description": self._description,
            "type": self._type,
            "dm_permission": self._dm_permission
        }
        _as_options = []
        if self._options:
            for option in self._options:
                _as_options.append(option.to_dict())
        if _as_options:
            _as_dict["options"] = _as_options
        return _as_dict

    
    