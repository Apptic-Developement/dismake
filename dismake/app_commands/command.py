from __future__ import annotations
import inspect
import re

from functools import partial, wraps
from typing import Any, Optional

from dismake.models.application_command import (
    ApplicationCommand,
    ApplicationCommandOption,
)

from ..types import AsyncFunction, SnowFlake
from ..enums import CommandType, OptionType

__all__ = ("SlashCommand", "Option", "Choice")

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
    def __init__(self, name: str, value: Optional[str] = None) -> None:
        self.name = name
        self.value = value or name

    def to_dict(self) -> dict[str, Any]:
        return {"name": self.name, "value": self.value}


class Option:
    _level: int = 1

    def __init__(
        self,
        name: str,
        type: int = OptionType.STRING,
        description: Optional[str] = "No description provided",
        name_localizations: Optional[dict[str, str]] = None,
        description_localizations: Optional[dict[str, str]] = None,
        required: Optional[bool] = None,
        choices: Optional[list[Choice]] = None,
        options: Optional[list[Option]] = None,
        channel_types: Optional[list[str]] = None,  # TODO: We will add son
        min_value: Optional[int] = None,
        max_value: Optional[int] = None,
        autocomplete: Optional[bool] = None,
    ) -> None:
        self.type = type
        self.name = validate_name(name)
        self.name_localizations = name_localizations
        self.description = description
        self.description_localizations = description_localizations
        self.required = required
        self.choices = choices
        self.options = options
        self.channel_types = channel_types  # TODO: We will add son
        self.min_value = min_value
        self.max_value = max_value
        self.autocomplete = autocomplete

        # Custom
        self.callback: Optional[AsyncFunction] = None
        self.autocomplete_callback: Optional[AsyncFunction] = None
        self.subcommands: dict[str, Option] = {}

    def sub_command(
        self,
        name: str,
        description: Optional[str] = None,
        name_localizations: Optional[dict[str, str]] = None,
        description_localizations: Optional[dict[str, str]] = None,
        options: Optional[list[Option]] = None,
    ):
        self.type = OptionType.SUB_COMMAND_GROUP
        command = Option(
            type=OptionType.SUB_COMMAND,
            name=name,
            description=description,
            name_localizations=name_localizations,
            description_localizations=description_localizations,
            options=options,
        )
        command._level = 1 + self._level
        if command._level > 2:
            raise RuntimeError(
                f"The {name!r} registration failed because it has too many nested levels. Please simplify the command structure and try again. Maximum allowed nesting level is 2."
            )

        def decorator(coro: AsyncFunction):
            @wraps(coro)
            def wrapper(*_, **__) -> Option:
                command.callback = coro
                self.subcommands[command.name] = command
                return command

            return wrapper()

        return decorator

    def to_dict(self) -> dict[str, Any]:
        base: dict[str, Any] = {
            "name": self.name,
            "description": self.description,
            "type": self.type,
        }

        if self.name_localizations is not None:
            base["name_localizations"] = self.name_localizations
        if self.description_localizations is not None:
            base["description_localizations"] = self.description_localizations

        # Prepare for only sub_commands
        if self.type in (OptionType.SUB_COMMAND, OptionType.SUB_COMMAND_GROUP):
            if self.type == OptionType.SUB_COMMAND_GROUP:
                if self.subcommands:
                    subcommands = list()
                    for command in self.subcommands.values():
                        subcommands.append(command.to_dict())
                    base["options"] = subcommands
                return base
            else:
                if self.options:
                    options = list()
                    for option in self.options:
                        options.append(option.to_dict())
                    base["options"] = options
                return base
        else:
            if self.required is not None:
                base["required"] = self.required
            if self.choices:
                choices = list()
                for choice in self.choices:
                    choices.append(choice.to_dict())
                base["choices"] = choices

            if self.options:
                options = [option.to_dict() for option in self.options]
                if options:
                    base["options"] = options

            if self.type in (OptionType.STRING, OptionType.INTEGER):
                if self.type == OptionType.STRING:
                    if self.min_value:
                        base["min_length"] = self.min_value
                    if self.max_value:
                        base["max_length"] = self.max_value
                else:
                    if self.min_value:
                        base["min_value"] = self.min_value
                    if self.max_value:
                        base["max_value"] = self.max_value
            if self.autocomplete is not None:
                base["autocomplete"] = self.autocomplete
            return base


class SlashCommand:
    def __init__(
        self,
        name: str,
        callback: AsyncFunction,
        type: int = CommandType.SLASH,
        description: Optional[str] = None,
        guild_id: Optional[SnowFlake] = None,
        name_localizations: Optional[dict[str, str]] = None,
        description_localizations: Optional[dict[str, str]] = None,
        options: Optional[list[Option]] = None,
        default_member_permissions: Optional[str] = None,
        dm_permission: Optional[bool] = None,
        nsfw: Optional[bool] = None,
    ) -> None:
        self.name = name
        self.type = type
        self.description = description or "No description provided."
        self.guild_id = guild_id
        self.name_localizations = name_localizations
        self.description_localizations = description_localizations
        self.options = options
        self.default_member_permissions = default_member_permissions
        self.dm_permission = dm_permission
        self.nsfw = nsfw
        self.callback: AsyncFunction = callback

        # Custom
        self.subcommands: dict[str, Option] = {}
        self._partial: Optional[ApplicationCommand] = None

    @property
    def partial(self) -> Optional[ApplicationCommand]:
        return self._partial

    def sub_command(
        self,
        name: str,
        description: Optional[str] = None,
        name_localizations: Optional[dict[str, str]] = None,
        description_localizations: Optional[dict[str, str]] = None,
        options: Optional[list[Option]] = None,
    ):
        command = Option(
            type=OptionType.SUB_COMMAND,
            name=name,
            description=description,
            name_localizations=name_localizations,
            description_localizations=description_localizations,
            options=options,
        )
        command._level = 1

        def decorator(coro: AsyncFunction):
            @wraps(coro)
            def wrapper(*_, **__) -> Option:
                command.callback = coro
                self.subcommands[command.name] = command
                return command

            return wrapper()

        return decorator

    def to_dict(self) -> dict[str, Any]:
        base = {
            "name": self.name,
            "description": self.description,
            "type": self.type,
        }
        options = list()
        if self.subcommands:
            for command in self.subcommands.values():
                options.append(command.to_dict())
        elif self.options:
            for option in self.options:
                options.append(option.to_dict())
        if options:
            base["options"] = options
        if self.default_member_permissions is not None:
            base["default_member_permissions"] = self.default_member_permissions

        if self.name_localizations is not None:
            base["name_localizations"] = self.name_localizations
        if self.description_localizations is not None:
            base["description_localizations"] = self.description_localizations

        if self.guild_id is not None:
            base["guild_id"] = self.guild_id

        if self.dm_permission is not None:
            base["dm_permission"] = self.dm_permission

        return base
