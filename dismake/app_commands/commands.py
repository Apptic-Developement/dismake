from __future__ import annotations
from typing import Any, TYPE_CHECKING, Generic, TypeVar
from enum import Enum

from ..permissions import Permissions
from ..types import AsyncFunction
from ..models import User, Member, Role

if TYPE_CHECKING:
    from ..types import AsyncFunction
    from ..permissions import Permissions


T = TypeVar("T")
__all__ = ("Command", "Option", "Choice", "Group")


class CommandType(Enum):
    SLASH = 1
    USER = 2
    MESSAGE = 3


class OptionType(Enum):
    SUB_COMMAND = 1
    SUB_COMMAND_GROUP = 2
    STRING = 3
    INTEGER = 4
    BOOLEAN = 5
    USER = 6
    CHANNEL = 7
    ROLE = 8
    MENTIONABLE = 9
    NUMBER = 10


_option_types = {
    User: OptionType.USER,
    Member: OptionType.USER,
    Role: OptionType.ROLE,
    str: OptionType.STRING,
    int: OptionType.INTEGER,
    bool: OptionType.BOOLEAN,
}


class Command:
    def __init__(
        self,
        name: str,
        description: str,
        callback: AsyncFunction,
        guild_id: int | None = None,
        name_localizations: dict[str, str] | None = None,
        description_localizations: dict[str, str] | None = None,
        options: list[Option] | None = None,
        default_member_permissions: Permissions | None = None,
        guild_only: bool | None = None,
        nsfw: bool | None = None,
    ) -> None:
        self.name = name
        self.description = description
        self.callback = callback
        self.guild_id = guild_id
        self.name_localizations = name_localizations
        self.description_localizations = description_localizations
        self.options = options
        self.default_member_permissions = default_member_permissions
        self.dm_permission = not guild_only
        self.nsfw = nsfw
        self.parent: Group | None = None
        self.type: CommandType | OptionType = (
            CommandType.SLASH if self.parent is not None else OptionType.SUB_COMMAND
        )

    def to_dict(self) -> dict[str, Any]:
        base = {
            "name": self.name,
            "description": self.description,
            "type": self.type.value,
            "options": [option.to_dict() for option in self.options]
            if self.options
            else [],
        }
        if self.parent is None:
            if self.guild_id is not None:
                base["guild_id"] = self.guild_id
            if self.name_localizations is not None:
                base["name_localizations"] = self.name_localizations
            if self.description_localizations is not None:
                base["description_localizations"] = self.description_localizations
            if self.default_member_permissions is not None:
                base[
                    "default_member_permissions"
                ] = self.default_member_permissions.value
            if self.dm_permission is not None:
                base["dm_permissions"] = self.dm_permission
            if self.nsfw is not None:
                base["nsfw"] = self.nsfw
        return base


class Group:
    def __init__(
        self,
        name: str,
        description: str,
        guild_id: int | None = None,
        name_localizations: dict[str, str] | None = None,
        description_localizations: dict[str, str] | None = None,
        default_member_permissions: Permissions | None = None,
        guild_only: bool | None = None,
        nsfw: bool | None = None,
        parent: Group | None = None,
    ) -> None:
        self.name = name
        self.description = description
        self.guild_id = guild_id
        self.name_localizations = name_localizations
        self.description_localizations = description_localizations
        self.default_member_permissions = default_member_permissions
        self.dm_permission = not guild_only
        self.nsfw = nsfw
        self.parent = parent
        self.type: CommandType | OptionType = (
            CommandType.SLASH if not self.parent else OptionType.SUB_COMMAND_GROUP
        )
        self.commands: dict[str, Command | Group] = {}
        if self.parent:
            if self.parent.parent:
                raise ValueError("groups can only be nested at most one level")
            self.parent.add_command(self)

        if len(self.commands.values()) > 25:
            raise TypeError("groups cannot have more than 25 commands")

    def add_command(self, command: Group | Command):
        if isinstance(command, Group) and self.parent:
            raise ValueError("groups can only be nested at most one level")

        self.commands[command.name] = command
        command.parent = self
        return command

    def command(
        self,
        name: str,
        description: str,
        *,
        guild_id: int | None = None,
        default_member_permissions: Permissions | None = None,
        guild_only: bool | None = None,
        nsfw: bool | None = None,
        options: list[Option] | None = None,
        name_localizations: dict[str, str] | None = None,
        description_localizations: dict[str, str] | None = None,
    ):
        def decorator(coro: AsyncFunction):
            command = Command(
                name=name,
                description=description,
                guild_id=guild_id,
                callback=coro,
                nsfw=nsfw,
                default_member_permissions=default_member_permissions,
                guild_only=guild_only,
                options=options,
                name_localizations=name_localizations,
                description_localizations=description_localizations,
            )
            return self.add_command(command)

        return decorator

    def to_dict(self) -> dict[str, Any]:
        base = {
            "name": self.name,
            "description": self.description,
            "type": self.type.value,
            "options": [command.to_dict() for command in self.commands.values()],
        }
        if self.parent is None:
            if self.guild_id is not None:
                base["guild_id"] = self.guild_id
            if self.name_localizations is not None:
                base["name_localizations"] = self.name_localizations
            if self.description_localizations is not None:
                base["description_localizations"] = self.description_localizations
            if self.default_member_permissions is not None:
                base[
                    "default_member_permissions"
                ] = self.default_member_permissions.value
            if self.dm_permission is not None:
                base["dm_permission"] = self.dm_permission
            if self.nsfw is not None:
                base["nsfw"] = self.nsfw
        return base


class Option(Generic[T]):
    def __init__(
        self,
        type: type,
        name: str,
        description: str,
        *,
        name_localizations: dict[str, str] | None = None,
        description_localizations: dict[str, str] | None = None,
        required: bool | None = None,
        choices: list[Choice] | None = None,
        options: list[Option] | None = None,
        channel_types: list[str] | None = None,
        min_value: int | None = None,
        max_value: int | None = None,
        autocomplete: bool | None = None,
    ) -> None:
        self.name = name
        self.description = description
        self.name_localizations = name_localizations
        self.description_localizations = description_localizations
        self.required = required
        self.choices = choices
        self.options = options
        self.channel_types = channel_types
        self.min_value = min_value
        self.max_value = max_value
        self.autocomplete = autocomplete
        try:
            self.type = _option_types[type]
        except:
            self.type = _option_types[str]

    def to_dict(self) -> dict[str, Any]:
        base = {
            "name": self.name,
            "description": self.description,
            "type": self.type.value,
        }
        if self.name_localizations is not None:
            base["name_localizations"] = self.name_localizations
        if self.description_localizations is not None:
            base["description_localizations"] = self.description_localizations
        if self.required is not None:
            base["required"] = self.required
        if self.choices is not None:
            base["choices"] = [choice.to_dict() for choice in self.choices]
        if self.options is not None:
            base["options"] = [option.to_dict() for option in self.options]
        if self.channel_types is not None:
            base["channel_types"] = self.channel_types
        if self.min_value is not None:
            base["min_value"] = self.min_value
        if self.max_value is not None:
            base["max_value"] = self.max_value
        if self.autocomplete is not None:
            base["autocomplete"] = self.autocomplete
        return base


class Choice:
    def __init__(
        self,
        name: str,
        name_localizations: dict[str, Any] | None = None,
        value: str | int | float | bool | None = None,
    ) -> None:
        self.name = name
        self.value = value or name
        self.name_localizations = name_localizations

    def to_dict(self) -> dict[str, Any]:
        base = {"name": self.name, "value": self.value}
        if self.name_localizations is not None:
            base.update({"name_localizations": self.name_localizations})
        return base
