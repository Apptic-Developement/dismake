from __future__ import annotations

import inspect
from typing import Any, TYPE_CHECKING, Annotated, get_origin


from ..permissions import Permissions
from ..types import AsyncFunction
from ..models import User, Member, Role
from .context import Context
from ..enums import CommandType, OptionType

if TYPE_CHECKING:
    from ..types import AsyncFunction
    from ..permissions import Permissions
    from ..plugin import Plugin


__all__ = ("Command", "Option", "Choice", "Group")


def _get_options(function: AsyncFunction) -> list[Option] | None:
    params = inspect.signature(function).parameters
    ret = list()
    for _, v in params.items():
        if v.default == inspect._empty and v.annotation is not None:
            if get_origin(v.annotation) == Annotated:
                args = v.annotation.__args__ + v.annotation.__metadata__
                if not len(args) > 2:
                    option = args[1]
                    if isinstance(option, Option):
                        ret.append(option)
    return ret


_option_types = {
    # fmt: off
    User:           OptionType.USER,
    Member:         OptionType.USER,
    Role:           OptionType.ROLE,
    str:            OptionType.STRING,
    int:            OptionType.INTEGER,
    bool:           OptionType.BOOLEAN,
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

    async def invoke(self, ctx: Context):
        opt_data = dict()
        options = ctx.get_options
        if options is None:
            return await self.callback(ctx)
        for option in options:
            if option.type in (
                OptionType.USER.value,
                OptionType.ROLE.value,
                OptionType.CHANNEL.value,
            ):
                if (data := ctx.data) is not None:
                    if (resolved := data.resolved) is not None:
                        if (
                            users := resolved.users
                        ) is not None and option.type == OptionType.USER.value:
                            opt_data[option.name] = users.get(str(option.value))
                        elif (
                            roles := resolved.roles
                        ) is not None and option.type == OptionType.ROLE.value:
                            opt_data[option.name] = roles.get(str(option.value))
            else:
                opt_data[option.name] = option.value
        args = list()
        for _, v in inspect.signature(self.callback).parameters.items():
            if v.default == inspect._empty:
                annotation = v.annotation
                if get_origin(annotation) == Annotated:
                    callback_params = annotation.__args__ + annotation.__metadata__
                    if len(callback_params) == 2:
                        option_object = callback_params[1].name
                        args.append(opt_data.get(option_object))
        args.insert(0, ctx)
        await self.callback(*tuple(args))

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
            return self.add_command(command)

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
        name: str,
        description: str,
        type: OptionType | type = str,
        *,
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
        self.description = description
        self.name_localizations = name_localizations
        self.description_localizations = description_localizations
        self.required = required
        self.choices = choices
        self.channel_types = channel_types
        self.min_value = min_value
        self.max_value = max_value
        self.autocomplete = autocomplete
        self.type: OptionType
        if isinstance(type, OptionType):
            self.type = type
        else:
            self.type = _option_types[type]

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
