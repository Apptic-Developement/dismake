from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Optional
from functools import wraps
from .commands import Command, Group
from .errors import PluginException

if TYPE_CHECKING:
    from .commands import Command, Group
    from .client import Bot
    from .types import AsyncFunction
    from .permissions import Permissions

__all__ = ("Plugin",)


class Plugin:
    """
    Represents a plugin.

    Plugins help you split your code into different files,
    similar to 'APIRouter' and discord.py's 'Cog'.

    Attributes
    ----------
    name: (str)
        The name of the plugin.
    default_member_permissions: (Permissions | None)
        This will override all the commands permissions with this permission.
    """
    def __init__(self, name: str = __name__, default_member_permissions: Permissions | None = None) -> None:
        self.name = name
        self.bot: Bot
        self._commands: dict[str, Command | Group] = {}
        self.error_handler: Optional[AsyncFunction] = None
        self._on_load: AsyncFunction | None = None
        self._events: dict[str, list[AsyncFunction]] = {}
        self.default_member_permissions = default_member_permissions

    def on_load(self, coro: AsyncFunction):
        @wraps(coro)
        def wrapper(*_, **__):
            if not asyncio.iscoroutinefunction(coro):
                raise PluginException(f"{coro.__name__!r} is not coroutine function.")
            self._on_load = coro 
            return coro
        return wrapper()

    def event(self, event_name: str | None = None):
        """
        A decorator that registers an event to listen to.

        Parameters
        ----------
        event_name: str
            The event name you want to listen.

        Example usage
        -------------
            >>> import dismake
            >>> plugin = dismake.Plugin()
            >>> @plugin.event()
            ... async def on_interaction():
            ...     print(f"A new interaction received.")
        """

        def decorator(coro: AsyncFunction):
            @wraps(coro)
            def wrapper(*_, **__):
                if not asyncio.iscoroutinefunction(coro):
                    raise PluginException(f"{coro.__name__!r} is not coroutine function.")
                name = event_name or coro.__name__
                if self._events.get(name) is not None:
                    self._events[name].append(coro)
                else:
                    self._events[name] = [coro]

            return wrapper()

        return decorator
    
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
                if not asyncio.iscoroutinefunction(coro):
                    raise PluginException(f"{coro.__name__!r} command callback must be a coroutine function.")
                
                if self.default_member_permissions is not None:
                    permissions = self.default_member_permissions
                elif default_member_permissions is not None:
                    permissions = default_member_permissions
                else:
                    permissions = None
                command = Command(
                    name=name,
                    description=description,
                    guild_id=guild_id,
                    callback=coro,
                    nsfw=nsfw,
                    default_member_permissions=permissions,
                    guild_only=guild_only,
                    name_localizations=name_localizations,
                    description_localizations=description_localizations,
                )
                command.plugin = self
                self._commands[command.name] = command
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
        if self.default_member_permissions is not None:
            permissions = self.default_member_permissions
        elif default_member_permissions is not None:
            permissions = default_member_permissions
        else:
            permissions = None
        command = Group(
            name=name,
            description=description,
            guild_id=guild_id,
            name_localizations=name_localizations,
            description_localizations=description_localizations,
            default_member_permissions=permissions,
            guild_only=guild_only,
            nsfw=nsfw,
            parent=parent,
        )
        command.plugin = self
        self._commands[command.name] = command
        return command

    def load(self, bot: Bot):
        bot._commands.update(self._commands)
        bot._events.update(self._events)
        if self._on_load is not None:
            asyncio.create_task(self._on_load())
        self.bot = bot
