from __future__ import annotations

import inspect
from typing import Any, TYPE_CHECKING, Annotated, Optional, get_origin
from functools import wraps

from .permissions import Permissions
from .types import AsyncFunction
from .models import (
    User,
    Member,
    Role,
    Channel,
    TextChannel,
    CategoryChannel,
    AnnouncementChannel,
    ApplicationCommandData,
)
from .errors import CommandInvokeError
from .enums import ChannelType, CommandType, OptionType, Locale

if TYPE_CHECKING:
    from .types import AsyncFunction
    from .permissions import Permissions
    from .plugin import Plugin
    from .models import Interaction


__all__ = ("Command", "Option", "Choice", "Group")


_option_types = {
    # fmt: off
    bool:           OptionType.BOOLEAN,
    int:            OptionType.INTEGER,
    str:            OptionType.STRING,
    User:           OptionType.USER,
    Member:         OptionType.USER,
    Role:           OptionType.ROLE,
    # Channels
    Channel:        OptionType.CHANNEL,
    TextChannel:        OptionType.CHANNEL,
    CategoryChannel:        OptionType.CHANNEL,
    AnnouncementChannel:        OptionType.CHANNEL,
}


def _get_options(func: AsyncFunction) -> list[Option]:
    """
    Extracts options from the given command callback.

    Parameters
    ----------
    func : AsyncFunction
        The function to get the options from.

    Returns
    -------
    list[Option]
        The options of the command.
    """
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


def _populate_locales(locale: dict[Locale, str]) -> dict[str, str]:
    locales = dict()
    for lang, value in locale.items():
        locales[lang.value] = value
    return locales


class Command:
    """
    Represents a Discord command or a Discord sub-command.

    Parameters
    ----------
    name (str):
        The name of the command/sub-command.
    description (str):
        A brief description of what the command/sub-command does.(Max length 100)
    callback (AsyncFunction):
        The function to be executed when the command is called.
    guild_id (int|None):
        The ID of the guild this command is registered in, or None if it's a global command.
    name_localizations (dict[str, str]|None):
        A dictionary of localized names for the command, keyed by language code.
    description_localizations (dict[str, str]|None):
        A dictionary of localized descriptions for the command, keyed by language code.
    default_member_permissions (Permissions|None):
        The default permissions required for members to execute the command.
    guild_only (bool|None):
        Whether the command can only be executed in a guild or not.
    dm_permission (bool):
        Whether the command can be executed in DMs or not.
    nsfw (bool|None):
        Whether the command can only be executed in channels marked as NSFW or not.
    """

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
        self.error_handler: Optional[AsyncFunction] = None

    def __str__(self) -> str:
        return self.name

    async def _invoke_error_handlers(
        self, interaction: Interaction, error: CommandInvokeError
    ):
        """
        Invokes the error handlers for the command.

        Parameters
        ----------
        interaction: Interaction
            The interaction that triggered the error.
        error: CommandInvokeError
            The error that triggered the command.
        """
        if self.error_handler is not None:
            return await self.error_handler(interaction, error)
        if self.plugin is not None and self.plugin.error_handler is not None:
            return await self.plugin.error_handler(interaction, error)
        if (bot_error_handler := interaction.bot.error_handler) is not None:
            return await bot_error_handler(interaction, error)

    async def invoke(self, interaction: Interaction):
        """
        Invokes the command.

        Parameters
        ----------
        interaction: Interaction
            The interaction that triggered the command.

        Raises
        ------
        CommandInvokeError
            The command failed to invoke.
        """
        args: tuple = tuple()
        kwargs: dict = dict()
        options = interaction.namespace.__dict__
        params = inspect.signature(self.callback).parameters
        for k, v in params.items():
            option: type | None = options.get(k)
            if option is not None:
                if v.default != inspect._empty:
                    kwargs[k] = option
                else:
                    args += (option,)
        try:
            await self.callback(interaction, *args, **kwargs)
        except Exception as e:
            assert interaction.data is not None and isinstance(
                interaction.data, ApplicationCommandData
            )
            exception = CommandInvokeError(self, e)
            return await self._invoke_error_handlers(interaction, exception)

    async def invoke_autocomplete(self, interaction: Interaction, name: str):
        """
        Invokes the autocomplete for the command.

        Parameters
        ----------
        interaction: Interaction
            The interaction that triggered the command.
        name: str
            The name of the option to autocomplete.

        Raises
        ------
        CommandInvokeError
            The command failed to invoke.
        """
        autocomplete = self.autocompletes.get(name)
        if not autocomplete:
            return

        choices: list[Choice] | None = await autocomplete(
            interaction, name=interaction.namespace.__dict__[name]
        )
        if choices is not None:
            return await interaction.autocomplete(choices)

    def autocomplete(self, option: str):
        """
        Decorator that registers an autocomplete for the command.

        Parameters
        ----------
        option: str
            The name of the option to autocomplete.

        Returns
        -------
        Callable[[AsyncFunction], AsyncFunction]
            The decorator.
        """

        def decorator(coro: AsyncFunction):
            @wraps(coro)
            def wrapper(*_, **__):
                self.autocompletes[option] = coro
                return coro

            return wrapper()

        return decorator

    def to_dict(self) -> dict[str, Any]:
        """
        Converts the command into a dictionary.

        Returns
        -------
        dict[str, Any]
            The dictionary.
        """
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
    """
    Represents a slash command group.

    Attributes
    ----------
    name (str):
        The name of the group.
    description (str):
        A brief description of what the group does.(Max length 100)
    guild_id (int|None):
        The ID of the guild this command is registered in, or None if it's a global command.
    name_localizations (dict[str, str]|None):
        A dictionary of localized names for the group, keyed by language code.
    description_localizations (dict[str, str]|None):
        A dictionary of localized descriptions for the group, keyed by language code.
    default_member_permissions (Permissions|None):
        The default permissions required for members to execute the group.
    guild_only (bool|None):
        Whether the group can only be executed in a guild or not.
    dm_permission (bool):
        Whether the group can be executed in DMs or not.
    nsfw (bool|None):
        Whether the group can only be executed in channels marked as NSFW or not.
    parent (Group|None):
        The parent group, if any.
    """

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
        """
        Adds a command to the group.

        Parameters
        ----------
        command: Group | Command
            The command to add.

        Raises
        ------
        TypeError
            The command is not a group or a command.
        ValueError
            The command is nested more than one level.
        """
        if isinstance(command, Group) and self.parent:
            raise ValueError("groups can only be nested at most one level")

        if not isinstance(command, (Group, Command)):
            raise TypeError("expected Group or Command but got %s" % type(command))
        self.commands[command.name] = command
        command.parent = self
        return command

    def command(
        self,
        name: str | None = None,
        description: str = "No description provided.",
        *,
        guild_id: int | None = None,
        default_member_permissions: Permissions | None = None,
        guild_only: bool | None = None,
        nsfw: bool | None = None,
        name_localizations: dict[str, str] | None = None,
        description_localizations: dict[str, str] | None = None,
    ):
        """
        Decorator that creates a sub command.

        Parameters
        ----------
        name: str | None
            The name of the command.
        description: str
            A brief description of what the command does.(Max length 100)
        guild_id: int | None
            The ID of the guild this command is registered in, or None if it's a global command.
        default_member_permissions: Permissions | None
            The default permissions required for members to execute the command.
        guild_only: bool | None
            Whether the command can only be executed in a guild or not.
        nsfw: bool | None
            Whether the command can only be executed in channels marked as NSFW or not.
        name_localizations: dict[str, str]|None
            A dictionary of localized names for the command, keyed by language code.
        description_localizations: dict[str, str]|None
            A dictionary of localized descriptions for the command, keyed by
        """

        def decorator(coro: AsyncFunction):
            command = Command(
                name=name or coro.__name__,
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
        """
        Decorator that creates a sub group.

        Parameters
        ----------
        name: str
            The name of the group.
        description: str
            A brief description of what the group does.(Max length 100)
        """
        command = Group(name=name, description=description, parent=self)
        return command

    def to_dict(self) -> dict[str, Any]:
        """
        Creates a dictionary representation of the group.

        Returns
        -------
        dict[str, Any]
            The dictionary representation of the group.
        """
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
    """
    Represents a slash command option.

    Attributes
    ----------
    name (str):
        The name of the option.
    description (str):
        The description of the option.
    name_localizations (dict[str, str]|None):
        A dictionary of localized names for the option, keyed by language code.
    description_localizations (dict[str, str]|None):
        A dictionary of localized descriptions for the option, keyed by language code.
    required (bool|None):
        Whether the option is required or not.
    choices (list[Choice]|None):
        A list of choices for the option.
    channel_types (list[ChannelType]|None):
        A list of channel types for the option.
    min_value (int|None):
        The minimum value for the option.
    max_value (int|None):
        The maximum value for the option.
    autocomplete (bool|None):
        Whether the option is an autocomplete option or not.
    """

    def __init__(
        self,
        name: str | None = None,
        description: str | None = None,
        name_localizations: dict[str, str] | None = None,
        description_localizations: dict[str, str] | None = None,
        required: bool | None = None,
        choices: list[Choice] | None = None,
        channel_types: list[ChannelType] = list(),
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
        """
        Creates a dictionary representation of the option.

        Returns
        -------
        dict[str, Any]
            The dictionary representation of the option.
        """
        base: dict[str, Any] = {
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
        if self.channel_types:
            base["channel_types"] = [t.value for t in self.channel_types]
        if self.min_value is not None:
            base["min_value"] = self.min_value
        if self.max_value is not None:
            base["max_value"] = self.max_value
        if self.autocomplete is not None:
            base["autocomplete"] = self.autocomplete
        return base


class Choice:
    """
    Represents a slash command choice.

    Attributes
    ----------
    name (str):
        The name of the choice.
    value (str):
        The value of the choice.
    name_localizations (dict[str, Any]|None):
        A dictionary of localized names for the choice, keyed by language code.
    """

    def __init__(
        self,
        name: str,
        name_localizations: dict[Locale, str] | None = None,
        value: str | int | float | bool | None = None,
    ) -> None:
        self.name = name
        self.value = value or name
        self.name_localizations = name_localizations

    def to_dict(self) -> dict[str, Any]:
        base: dict[str, Any] = {"name": self.name, "value": self.value}
        if self.name_localizations is not None:
            base["name_localizations"] = _populate_locales(self.name_localizations)
        return base
