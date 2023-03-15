from __future__ import annotations

from typing import Optional
from functools import wraps

from ..enums import CommandType, OptionType
from ..types import AsyncFunction, SnowFlake
from .command import validate_name, Option

__all__ = ("Group", "GroupCommand")


class Group:
    def __init__(
        self,
        name: str,
        description: str,
        parent: Optional[Group] = None,
        guild_id: Optional[SnowFlake] = None,
        name_localizations: Optional[dict[str, str]] = None,
        description_localizations: Optional[dict[str, str]] = None,
        options: Optional[list[Option]] = None,
        default_member_permissions: Optional[str] = None,
        nsfw: Optional[bool] = None,
        dm_permission: Optional[bool] = None,
    ) -> None:
        self._name = validate_name(name)
        self._description = description
        self._parent = parent
        self._guild_id = guild_id
        self._commands: list[GroupCommand] = []
        self._name_localizations = name_localizations
        self._description_localizations = description_localizations
        self._options = options
        self._default_member_permissions = default_member_permissions
        self._nsfw = nsfw
        self._dm_permission = dm_permission
        if parent:
            self._type = OptionType.SUB_COMMAND_GROUP
        else:
            self._type = CommandType.SLASH

    def command(self, name: str, description: str):
        command = GroupCommand(name, description)

        def decorator(coro: AsyncFunction):
            @wraps(coro)
            def wrapper(*_, **__):
                self._commands.append(command)
                return command

            return wrapper()

        return decorator

    # @property
    # def payload(self):
    #     payload = {}
    #     options = []
    #     if self._parent:

    #         payload.update(
    #             {
    #                 "name": self._parent._name,
    #                 "description": self._parent._description,
    #                 "type": self._parent._type,
    #             }
    #         )
    #         self_options = []
    #         for command in self._commands:
    #             self_options.append(command.payload)
    #         options.append(
    #             {
    #                 "name": self._name,
    #                 "description": self._description,
    #                 "type": self._type,
    #                 "options": self_options,
    #             }
    #         )
    #         if self._name_localizations:
    #             payload["name_localizations"] = self._name_localizations
    #         if self._description_localizations:
    #             payload["description_localization"] = self._description_localizations
    #         if self._guild_id:
    #             payload["guild_id"] = self._guild_id
    #         payload["options"] = options
    #         return payload

    #     else:
    #         payload.update(
    #             {"name": self._name, "description": self._description, "type": self._type}
    #         )
    #         for command in self._commands:
    #             options.append(command.payload)

    #         if options:
    #             payload["options"] = options

    #         return payload
    @property
    def payload(self):
        payload = {
            "name": self
        }


class GroupCommand:
    def __init__(
        self, name: str, description: str, options: Optional[list[Option]] = None, name_localizations: Optional[dict[str, str]] = None,
        description_localizations: Optional[dict[str, str]] = None,
    ) -> None:
        self._name = name
        self._description = description
        self._type = OptionType.SUB_COMMAND
        self._options = options
        self._name_localizations = name_localizations,
        self._description_localizations = description_localizations,
        self._callback: Optional[AsyncFunction] = None

    @property
    def callback(self) -> Optional[AsyncFunction]:
        return self._callback

    @property
    def payload(self):
        payload = {
            "type": self._type,
            "name": self._name,
            "description": self._description,
        }
        if self._options:
            options = []
            for option in self._options:
                options.append(option.payload)
            if options:  # For Saftey
                payload["options"] = options
        if self._name_localizations:
            payload["name_localizations"] = self._name_localizations
        if self._description_localizations:
            payload["description_localization"] = self._description_localizations
        return payload
