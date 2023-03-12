from __future__ import annotations

from typing import Any, Optional
from functools import wraps
from .enums import OptionType, CommandType
from dismake.types.snowflake import SnowFlake
from .types import AsyncFunction

__all__ = ("SlashCommand", "Option", "Choice")


async def _default_slash_command_callback(*args, **kwargs):
    # TODO: Response
    pass


class Choice:
    def __init__(
        self,
        name: str,
        value: str | int | float,
        name_localizations: list[dict] | None = None,
    ) -> None:
        self._name = name
        self._value = value
        self._name_localizations = name_localizations

    def _to_dict(self) -> dict[str, Any]:
        return {
            "name": self._name,
            "value": self._value,
            "name_localizations": self._name_localizations,
        }


class Option:
    _level: int = 0

    def __init__(
        self,
        name: str,
        description: Optional[str],
        type: int = OptionType.STRING.value,
        required: bool = False,
        autocomplete: bool = False,
        autocompleter: Optional[AsyncFunction] = None,
        choices: list[Choice] | None = None,
        min_value: int | None = None,
        max_value: int | None = None,
        channel_types: int | None = None,
    ) -> None:
        self._name = name
        self._description = description or "No description provided."
        self._type = type
        self._required = required
        self._autocomplete = autocomplete
        self._autocompleter = autocompleter
        self._choices = choices
        self._min_value = min_value
        self._max_value = max_value
        self._channel_types = channel_types
        self._options: list[Option] = list()
        self._group_commands: dict[str, Option] = {}
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
            "autocomplete": self._autocomplete,
        }
        _as_options = []
        if self._choices:
            _as_choices = []
            for choice in self._choices:
                _as_choices.append({"name": choice._name, "value": choice._value})
            _as_dict["choices"] = _as_choices

        if self._options:
            for option in self._options:
                if (
                    option._type != OptionType.SUB_COMMAND
                    or option._type != OptionType.SUB_COMMAND_GROUP
                ):
                    _as_options.append(option.to_dict())

        if self._group_commands:
            for _, gcommand in self._group_commands.items():
                if gcommand._type != OptionType.SUB_COMMAND_GROUP:
                    _as_options.append(gcommand.to_dict())
        _as_dict["options"] = _as_options
        return _as_dict

    def command(
        self,
        name: str,
        description: Optional[str],
        options: Optional[list[Option]] = None,
    ):
        command = Option(
            name=name, description=description, type=OptionType.SUB_COMMAND.value
        )
        command._level = self._level + 1
        if options:
            for option in options:
                if (
                    option._type != OptionType.SUB_COMMAND
                    or option._type != OptionType.SUB_COMMAND
                ):
                    command._options.append(option)

        if self._level >= 2:
            raise RuntimeError("Sub commands cannot be three levels deep")
        
        def decorator(coro: AsyncFunction):
            @wraps(coro)
            def wrapper(*args, **kwargs):
                command.callback = coro
                self._group_commands[command._name] = command
                # Reset and make this option a group
                self._options.clear()
                self._type = OptionType.SUB_COMMAND_GROUP
                return command

            return wrapper()

        return decorator


class SlashCommand:
    _level: int = 0

    def __init__(
        self,
        *,
        name: str,
        description: Optional[str],
        application_id: Optional[int] = None,
        guild_id: Optional[SnowFlake] = None,
        name_localizations: Optional[dict[str, str]] = None,
        description_localizations: Optional[dict[str, str]] = None,
        default_member_permissions: Optional[str] = None,
        dm_permission: Optional[bool] = True,
        default_permission: Optional[bool] = True,
        nsfw: Optional[bool] = False,
    ) -> None:
        self._id: Optional[SnowFlake] = None
        self._name = name
        self._description = description or "No description provided."
        self._type = CommandType.SLASH.value
        self._application_id = application_id
        self._guild_id = guild_id
        self._name_localizations = name_localizations
        self._description_localizations = description_localizations
        self._options: list[Option] = list()
        self._default_member_permissions = default_member_permissions
        self._dm_permission = dm_permission
        self._default_permission = default_permission
        self._nsfw = nsfw
        self._options: list[Option] = list()
        self._subcommands: dict[str, Option] = {}
        self._callback: AsyncFunction | None = _default_slash_command_callback

    def __str__(self) -> str:
        return f"<Command name='{self._name}' description='{self._description}'>"

    @property
    def id(self) -> int | str | None:
        return self._id
    
    @id.setter
    def id(self, value):
        self._id = value
    
    @property
    def callback(self) -> Optional[AsyncFunction]:
        return self._callback

    @callback.setter
    def callback(self, value: AsyncFunction | None):
        if value is None:
            self._callback = _default_slash_command_callback
            return
        self._callback = value

    def command(
        self,
        name: str,
        description: Optional[str],
        options: Optional[list[Option]] = None,
    ):
        if name in self._subcommands.keys():
            raise ValueError(
                f"{name!r} already registered as a slash command please use a different name."
            )
        
        command = Option(
            name=name, description=description, type=OptionType.SUB_COMMAND.value
        )
        if options:
            for option in options:
                if (
                    option._type != OptionType.SUB_COMMAND
                    or option._type != OptionType.SUB_COMMAND
                ):
                    command._options.append(option)

        def decorator(coro: AsyncFunction):
            @wraps(coro)
            def wrapper(*args, **kwargs):
                command._callback = coro

                command._level = 1

                # Reset some value of self
                self._options.clear()
                self._callback = None
                self._subcommands[name] = command
                return command

            return wrapper()

        return decorator

    def to_dict(self) -> dict:
        _as_dict = {
            "name": self._name,
            "description": self._description,
            "type": self._type,
            "dm_permission": self._dm_permission,
            "guild_id": self._guild_id,
        }
        _as_options = []
        if self._options:
            for option in self._options:
                _as_options.append(option.to_dict())

        elif self._subcommands:
            for _, _sub_command in self._subcommands.items():
                _as_options.append(_sub_command.to_dict())
        if _as_options:
            _as_dict["options"] = _as_options
        return _as_dict
