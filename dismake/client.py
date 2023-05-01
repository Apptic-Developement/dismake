from __future__ import annotations
import asyncio
from functools import wraps
from logging import getLogger
from functools import wraps
from typing import Any, List, Dict, Optional, TYPE_CHECKING, Callable, Coroutine, Union
from fastapi import FastAPI
from .models import Guild
from .handler import InteractionHandler
from .http import HttpClient
from .models import User
from .utils import LOGGING_CONFIG
from .commands import SlashCommand
from .errors import CommandInvokeError
from .app_commands import Command, Group

if TYPE_CHECKING:
    from .commands import Context
    from .ui import House, Component
    from .types import AsyncFunction, SnowFlake
    from .app_commands import Option
    from .permissions import Permissions


log = getLogger("uvicorn")
__all__ = ("Bot",)


class Bot(FastAPI):
    """
    A class for creating a Discord bot using FastAPI.

    Parameters
    ----------
    token : str
        The Discord bot's token.
    client_public_key : str
        The Discord client's public key.
    client_id : int
        The Discord client's ID.
    route : str
        The route to listen for Discord interactions on, by default "/interactions".
    interaction_handler : Optional[InteractionHandler]
        An interaction handler to process incoming Discord interactions, by default None.
    **kwargs
        Additional keyword arguments that will be passed to the FastAPI constructor.
    """

    def __init__(
        self,
        token: str,
        client_public_key: str,
        client_id: int,
        route: str = "/interactions",
        interaction_handler: Optional[InteractionHandler] = None,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self._client_id = client_id
        self._client_public_key = client_public_key
        self._interaction_handler = interaction_handler or InteractionHandler(self)
        self._http = HttpClient(token=token, client_id=client_id)
        self.add_route(
            path=route,
            route=self._interaction_handler.handle_interactions,
            methods=["POST"],
            include_in_schema=False,
        )
        self.add_event_handler("startup", self._http.fetch_me)
        self._events: Dict[str, List[AsyncFunction]] = {}
        self.add_event_handler("startup", lambda: self.dispatch("ready"))
        self._slash_commands: Dict[str, SlashCommand] = {}
        self._components: Dict[str, Component] = {}
        self._error_handler: Callable[
            [Context, Exception], Coroutine[Any, Any, Any]
        ] = self._default_error_handler

        # Slash Commands
        self._app_commands: Dict[str, Union[Group, Command]] = {}

    @property
    def user(self) -> User:
        """
        Returns the user object representing the bot.

        Returns
        -------
        User
            The user object representing the bot.
        """
        return self._http._user

    def get_command(self, name: str) -> Optional[SlashCommand]:
        """
        Get a SlashCommand object with the specified name.

        Parameters
        ----------
        name : str
            The name of the SlashCommand object to retrieve.

        Returns
        -------
        Optional[SlashCommand]
            The SlashCommand object with the specified name, or None if no such object exists.
        """
        return self._slash_commands.get(name)

    def run(self, **kwargs):
        import uvicorn

        kwargs["log_config"] = kwargs.get("log_config", LOGGING_CONFIG)
        uvicorn.run(**kwargs)

    async def _dispatch_callback(self, coro: AsyncFunction, *args, **kwargs):
        try:
            await coro(*args, **kwargs)
        except Exception as e:
            log.error("An error occured in %s" % coro.__name__, exc_info=e)

    def dispatch(self, event_name: str, *args, **kwargs):
        event = self._events.get(event_name)
        if not event:
            return
        for coro in event:
            asyncio.ensure_future(self._dispatch_callback(coro, *args, **kwargs))

    def event(self, event_name: str):
        def decorator(coro: AsyncFunction):
            @wraps(coro)
            def wrapper(*_, **__):
                if self._events.get(event_name) is not None:
                    self._events[event_name].append(coro)
                else:
                    self._events[event_name] = [coro]

            return wrapper()

        return decorator

    def add_command(self, command: SlashCommand):
        if self._slash_commands.get(command.name):
            raise ValueError(
                f"You can not create more than one command with same name."
            )
        self._slash_commands[command.name] = command

    def add_commands(self, commands: List[SlashCommand]):
        for command in commands:
            self.add_command(command)

    async def sync_commands(self, guild_ids: Optional[SnowFlake] = None):
        return await self._http.bulk_override_commands(
            [command for command in self._slash_commands.values()]
        )

    def on_app_command_error(self, coro: AsyncFunction):
        @wraps(coro)
        def wrapper(*_, **__):
            self._error_handler = coro
            return coro

        return wrapper()

    async def _default_error_handler(self, ctx: Context, error: Exception) -> Any:
        if isinstance(error, CommandInvokeError):
            await ctx.respond(
                f"Oops! Something went wrong while running the command.", ephemeral=True
            )
        raise error

    async def fetch_guild(self, guild_id: int) -> Guild:
        res = await self._http.client.request(method="GET", url=f"/guilds/{guild_id}")
        res.raise_for_status()
        return Guild(**res.json())

    def add_house(self, house: House) -> None:
        if not (components := house.components):
            return
        for component in components:
            if self._components.get((custom_id := component.custom_id)):
                continue
            self._components[custom_id] = component

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
                    options=options,
                    name_localizations=name_localizations,
                    description_localizations=description_localizations,
                )
                self._app_commands[command.name] = command

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
        self._app_commands[command.name] = command
        return command
