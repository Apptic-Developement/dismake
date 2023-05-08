from __future__ import annotations

import inspect
from typing import Any, TYPE_CHECKING, Annotated, Callable, Coroutine, get_origin
from functools import wraps

from ..permissions import Permissions
from ..types import AsyncFunction
from ..models import User, Member, Role
from ..enums import CommandType, OptionType

if TYPE_CHECKING:
    from ..types import AsyncFunction
    from ..permissions import Permissions
    from ..plugin import Plugin
    from ..models import Interaction, ApplicationCommandOption


__all__ = ("Command", "Option", "Choice", "Group")

_option_types = {
    # fmt: off
    User:           OptionType.USER,
    Member:         OptionType.USER,
    Role:           OptionType.ROLE,
    str:            OptionType.STRING,
    int:            OptionType.INTEGER,
    bool:           OptionType.BOOLEAN,
}


def _get_options(func: AsyncFunction):
    params = inspect.signature(func).parameters
    options: list[Option] = list()
    for k, v in params.items():
        # k: The name of the function
        #     - name
        # v: The annotation of the function
        #     - typing.Annotated[str, <Option name="foo">]
        annotation = v.annotation
        if get_origin(annotation) != Annotated:
            continue
        option_type: type = annotation.__args__[0]
        option_object: Option = annotation.__metadata__[0]
        option_object.type = _option_types[option_type]
        if option_object.description is None:
            option_object.description = "..."

        if option_object.name is None:
            option_object.name = k

        if option_object.required is None:
            if v.default != inspect._empty:
                option_object.required = False
            else:
                option_object.required = True

        options.append(option_object)
    return options


class Command:
    def __init__(
        self,
        name: str,
        description: str,
        callback: AsyncFunction,
        guild_id: int | None = None,
        name_localizations: dict[str, str] | None = None,
        description_localizations: dict[str, str] | None = None,
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
        self.default_member_permissions = default_member_permissions
        self.dm_permission = not guild_only
        self.nsfw = nsfw
        self.parent: Group | None = None
        self.type: CommandType | OptionType = (
            CommandType.SLASH if self.parent is not None else OptionType.SUB_COMMAND
        )
        self.options = _get_options(self.callback)
        self.plugin: Plugin | None = None
        self.autocompletes: dict[str, AsyncFunction] = {}

    def __str__(self) -> str:
        return self.name

    async def invoke(self, interaction: Interaction):
        args = tuple()
        kwargs = dict()
        options = interaction.namespace.__dict__
        params = inspect.signature(self.callback).parameters
        for k, v in params.items():
            option: type | None = options.get(k)
            if option is not None:
                if v.default != inspect._empty:
                    kwargs[k] = option
                else:
                    args += (option,)
        await self.callback(interaction, *args, **kwargs)

    async def invoke_autocomplete(self, interaction: Interaction, name: str):
        autocomplete = self.autocompletes.get(name)
        if not autocomplete:
            return

        choices: list[Choice] | None = await autocomplete(interaction)
        if choices is not None:
            return await interaction.autocomplete(choices)

    def autocomplete(self, option: str):
        def decorator(coro: AsyncFunction):
            @wraps(coro)
            def wrapper(*_, **__):
                self.autocompletes[option] = coro
                return coro

            return wrapper()

        return decorator

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
        self.plugin: Plugin | None = None
        if self.parent:
            if self.parent.parent:
                raise ValueError("groups can only be nested at most one level")
            self.parent.add_command(self)

        if len(self.commands.values()) > 25:
            raise TypeError("groups cannot have more than 25 commands")

    def __str__(self) -> str:
        return self.name

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
                name_localizations=name_localizations,
                description_localizations=description_localizations,
            )
            self.add_command(command)
            return command

        return decorator

    def create_sub_group(self, name: str, description: str):
        command = Group(name=name, description=description, parent=self)
        return command

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


class Option:
    def __init__(
        self,
        name: str | None = None,
        description: str | None = None,
        name_localizations: dict[str, str] | None = None,
        description_localizations: dict[str, str] | None = None,
        required: bool | None = None,
        choices: list[Choice] | None = None,
        channel_types: list[str] | None = None,
        min_value: int | None = None,
        max_value: int | None = None,
        autocomplete: bool | None = None,
    ) -> None:
        self.name = name
        self.description = description or "..."
        self.name_localizations = name_localizations
        self.description_localizations = description_localizations
        self.required = required
        self.choices = choices
        self.channel_types = channel_types
        self.min_value = min_value
        self.max_value = max_value
        self.autocomplete = autocomplete
        self.type: OptionType = OptionType.STRING

    def __repr__(self) -> str:
        return f"<Option name={self.name}>"

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
