from __future__ import annotations

from typing import TYPE_CHECKING, Any, Generic, TypeVar

from .base import _BaseAppCommand
from ..enums import CommandType, OptionType
if TYPE_CHECKING:
    from ..types import AsyncFunction
    from ..permissions import Permissions

__all__ = ("AppCommand", "Group")

T = TypeVar("T")


class Choice:
    def __init__(
        self,
        name: str,
        name_localizations: dict[str, Any] | None,
        value: int | str | float | bool | None,
    ) -> None:
        self.name = name
        self.name_localizations = name_localizations
        self.value = value or name

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "value": self.value,
            "name_localizations": self.name_localizations,
        }


class Option(Generic[T]):
    def __init__(
        self,
        name: str,
        description: str | None = "No description provided",
        *,
        type: OptionType | None = None,
        name_localizations: dict[str, str] | None = None,
        description_localizations: dict[str, str] | None = None,
        required: bool = False,
        choices: list[Choice] | None = None,
        options: list[Option] | None = None,
        channel_types: list[str] | None = None,
        min_value: int | None = None,
        max_value: int | None = None,
        autocomplete: bool | None = None,
    ) -> None:
        self.name = name
        self.description = description
        self.type = type or OptionType.STRING
        self.name_localizations = name_localizations
        self.description_localizations = description_localizations
        self.required = required
        self.choices = choices
        self.options = options
        self.channel_types = channel_types
        self.min_value = min_value
        self.max_value = max_value
        self.autocomplete = autocomplete

    def to_dict(self) -> dict[str, Any]:
        ...


class AppCommand(_BaseAppCommand):
    def __init__(
        self,
        name: str,
        description: str,
        *,
        name_localizations: dict[str, str] | None = None,
        description_localizations: dict[str, str] | None = None,
        callback: AsyncFunction | None = None,
        options: list[Option] | None = None,
        default_member_permissions: Permissions | None = None,
        dm_permission: bool | None = None,
        nsfw: bool | None = None,
        guild_id: int | None = None,
    ) -> None:
        super().__init__(
            name, description, name_localizations, description_localizations
        )
        self._children: list[AppCommand] = list()
        self._parent: Group | None = None
        self.callback = callback
        self.options = options
        self.default_member_permissions = default_member_permissions
        self.dm_permission = dm_permission
        self.nsfw = nsfw
        self.guild_id = guild_id
        self.type: CommandType | OptionType = (
            CommandType.SLASH if self.parent is None else OptionType.SUB_COMMAND
        )

    @property
    def parent(self) -> Group | None:
        return self._parent

    @parent.setter
    def parent(self, group: Group) -> None:
        self._parent = group

    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base["type"] = self.type.value
        if self.options is not None:
            base["options"] = [option.to_dict() for option in self.options]
        if not self.parent:
            if self.default_member_permissions is not None:
                base[
                    "default_member_permissions"
                ] = self.default_member_permissions.value
            if self.dm_permission is not None:
                base["dm_permission"] = self.dm_permission
            if self.nsfw is not None:
                base["nsfw"] = self.nsfw
            if self.guild_id is not None:
                base["guild_id"] = self.guild_id

        return base


class Group(_BaseAppCommand):
    def __init__(
        self,
        name: str,
        description: str,
        *,
        parent: Group | None = None,
        name_localizations: dict[str, str] | None = None,
        description_localizations: dict[str, str] | None = None,
        default_member_permissions: Permissions | None = None,
        guild_only: bool | None = None,
        nsfw: bool | None = None,
        guild_id: int | None = None,
    ) -> None:
        super().__init__(
            name, description, name_localizations, description_localizations
        )
        self.default_member_permissions = default_member_permissions
        self.dm_permission = guild_only
        self.nsfw = nsfw
        self.guild_id = guild_id
        self._parent = parent
        self._children: list[AppCommand | Group] = list()
        self.type: CommandType | OptionType = (
            CommandType.SLASH if self.parent is None else OptionType.SUB_COMMAND_GROUP
        )
        if self.parent is not None:
            if self.parent.parent is not None:
                raise ValueError("groups can only be nested at most one level")
            self.parent.add_command(self)

    def add_command(self, command: Group | AppCommand) -> Group | AppCommand:
        if isinstance(command, Group) and self.parent is not None:
            raise ValueError("groups can only be nested at most one level")
        self._children.append(command)
        command.parent = self
        return command

    @property
    def parent(self) -> Group | None:
        return self._parent

    @parent.setter
    def parent(self, group: Group) -> None:
        self._parent = group

    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base["type"] = self.type.value
        if self._children is not None:
            base["options"] = [child.to_dict() for child in self._children]
        if self.parent is None:
            if not self.parent:
                if self.default_member_permissions is not None:
                    base[
                        "default_member_permissions"
                    ] = self.default_member_permissions.value
                if self.dm_permission is not None:
                    base["dm_permission"] = self.dm_permission
                if self.nsfw is not None:
                    base["nsfw"] = self.nsfw
                if self.guild_id is not None:
                    base["guild_id"] = self.guild_id
        return base
