from __future__ import annotations
from functools import wraps
import re
from typing import Any, Optional

from ..types import AsyncFunction, SnowFlake
from ..enums import CommandType, OptionType

__all__ = ("SlashCommand", "Option", "Choice", "validate_name")

THAI_COMBINING = r"\u0e31-\u0e3a\u0e47-\u0e4e"
DEVANAGARI_COMBINING = r"\u0900-\u0903\u093a\u093b\u093c\u093e\u093f\u0940-\u094f\u0955\u0956\u0957\u0962\u0963"
VALID_NAME = re.compile(r"^[-_\w" + THAI_COMBINING + DEVANAGARI_COMBINING + r"]{1,32}$")


def validate_name(name: str):
    if VALID_NAME.match(name) is None:
        raise NameError(
            f"{name!r} must be between 1-32 characters and contain only lower-case letters, numbers, hyphens, or underscores."
        )
    return name


class Choice:
    def __init__(self, name: str, value: Optional[str | int | float] = None) -> None:
        self.name = name
        self.value = value

    def to_dict(self):
        return {"name": self.name, "value": self.value if self.value else self.name}


class Option:
    _level: int = 0
    def __init__(
        self,
        name: str,
        description: str,
        type: int = OptionType.STRING,
        name_localizations: Optional[dict[str, str]] = None,
        description_localizations: Optional[dict[str, str]] = None,
        required: Optional[bool] = False,
        choices: Optional[list[Choice]] = None,
        options: Optional[list[Option]] = None,
        # channel_types: Optional[list[str]] = None,
        min_length: Optional[int] = None,
        max_length: Optional[int] = None,
        autocomplete: Optional[bool] = None,
        autocomplete_callback: Optional[AsyncFunction] = None,
    ) -> None:
        self._type = type
        self._name = validate_name(name)
        self._description = description
        self._name_localizations = name_localizations
        self._description_localizations = description_localizations
        self._required = required
        self._choices = choices
        # self._channel_types = channel_types
        self._min_length = min_length
        self._max_length = max_length
        self._autocomplete = autocomplete
        self._options = options
        self._callback: AsyncFunction |None = None
        self._sub_commands: list[Option] = (
            [command for command in options if command._type == OptionType.SUB_COMMAND]
            if options
            else []
        )
        self._autocomplete_callback = autocomplete_callback

    def command(
        self,
        name: str,
        description: str,
        options: Optional[list[Option]] = None
    ):
        self._type = OptionType.SUB_COMMAND_GROUP
        command = Option(
            name=name,
            description=description,
            options=options,
            type=OptionType.SUB_COMMAND
        )
        if self._options: self._options.clear()
        if self._callback: self._callback = None
        command._level = 1 + self._level
        if self._level > 1:
            raise RuntimeError("A slash command can have max 2 childs.")
        def decorator(coro: AsyncFunction):
            @wraps(coro)
            def wrapper(*_, **__):
                self._sub_commands.append(command)
                return command
            return wrapper()
        return decorator
    

    def to_dict(self):
        payload = {
            "type": self._type,
            "name": self._name,
            "description": self._description,
        }
        if self._name_localizations:
            payload["name_localization"] = self._name_localizations

        if self._description_localizations:
            payload["description_localization"] = self._description_localizations

        if self._required is not None:
            payload["required"] = self._required

        if self._choices:
            choices = []
            for choice in self._choices:
                choices.append(choice.to_dict())

            if choices:  # Saftey
                payload["choices"] = choices

        if self._type == OptionType.STRING:
            if self._min_length:
                payload["min_length"] = self._min_length

            if self._max_length:
                payload["max_length"] = self._max_length
        elif self._type == OptionType.INTEGER:
            if self._min_length:
                payload["min_value"] = self._min_length

            if self._max_length:
                payload["max_value"] = self._max_length

        if self._autocomplete and self._autocomplete_callback:
            payload["autocomplete"] = self._autocomplete
        
        options = []
        if self._sub_commands:
            for command in self._sub_commands:
                options.append(command.to_dict())
        if self._options:
            for opt in self._options:
                options.append(opt.to_dict())

        if options:
            payload["options"] = options
        return payload


class SlashCommand:
    def __init__(
        self,
        name: str,
        description: str,
        guild_id: Optional[SnowFlake] = None,
        name_localizations: Optional[dict[str, str]] = None,
        description_localizations: Optional[dict[str, str]] = None,
        options: Optional[list[Option]] = None,
        default_member_permissions: Optional[str] = None,
        nsfw: Optional[bool] = None,
        dm_permission: Optional[bool] = None,
    ) -> None:
        self._name = validate_name(name)
        self._type = CommandType.SLASH
        self._description = description
        self._guild_id = guild_id
        self._name_localizations = name_localizations
        self._description_localizations = description_localizations
        self._options = options
        self._default_member_permissions = default_member_permissions
        self._nsfw = nsfw
        self._dm_permission = dm_permission
        self._callback: Optional[AsyncFunction] = None
        self._subcommands: list[Option] = []

    @property
    def callback(self) -> Optional[AsyncFunction]:
        return self._callback


    def sub_command(
        self,
        name: str,
        description: str,
        options: Optional[list[Option]] = None
    ):

        command = Option(
            name=name,
            description=description,
            options=options,
            type=OptionType.SUB_COMMAND
        )
        if self._options: self._options.clear()
        if self._callback: self._callback = None
        command._level = 1 + command._level
        if command._level > 1:
            raise RuntimeError("Max childs reached")

        def decorator(coro: AsyncFunction):
            @wraps(coro)
            def wrapper(*_, **__):
                self._subcommands.append(command)
                return command
            return wrapper()
        return decorator


    def to_dict(self):
        payload: dict[str, Any] = {
            "name": self._name,
            "description": self._description,
            "type": self._type,
        }
        if self._guild_id:
            payload["guild_id"] = self._guild_id

        if self._name_localizations:
            payload["name_localizations"] = self._name_localizations
        if self._description_localizations:
            payload["description_localizations"] = self._description_localizations

        options = []
        if self._options:
            for option in self._options:
                if option._type not in (
                    OptionType.SUB_COMMAND,
                    OptionType.SUB_COMMAND_GROUP,
                ):
                    options.append(option.to_dict())
        if self._subcommands:
            for command in self._subcommands:
                options.append(command.to_dict())

        if options:
            payload["options"] = options

        return payload
