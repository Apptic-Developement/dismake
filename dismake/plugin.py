from __future__ import annotations

from typing import TYPE_CHECKING
from functools import wraps
from .permissions import Permissions
from .types import AsyncFunction
from .app_commands import Command, Group

if TYPE_CHECKING:
    from .app_commands import Command, Group
    from .client import Bot
__all__ = ("Plugin",)


class Plugin:
    def __init__(self, name: str = __name__) -> None:
        self.name = name
        self.bot: Bot
        self._app_commands: dict[str, Command | Group] = {}

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
            @wraps(coro)
            def wrapper(*_, **__):
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
                command.plugin = self
                self._app_commands[command.name] = command
                return command

            return wrapper()

        return decorator

    def create_group(
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
    ):
        command = Group(
            name=name,
            description=description,
            guild_id=guild_id,
            name_localizations=name_localizations,
            description_localizations=description_localizations,
            default_member_permissions=default_member_permissions,
            guild_only=guild_only,
            nsfw=nsfw,
            parent=parent,
        )
        command.plugin = self
        self._app_commands[command.name] = command
        return command

    def load(self, bot: Bot):
        bot._app_commands.update(self._app_commands)
        self.bot = bot
