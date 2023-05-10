from __future__ import annotations
import asyncio
from functools import wraps
from functools import wraps
from typing import Any, List, Dict, Optional, TYPE_CHECKING, Union
from fastapi import FastAPI
from .models import Guild
from .handler import InteractionHandler
from .http import HttpClient
from .models import User
from .errors import CommandInvokeError
from .app_commands import Command, Group
from .utils import LOGGING_CONFIG, getLogger


if TYPE_CHECKING:
    from .ui import House, Component
    from .types import AsyncFunction
    from .permissions import Permissions
    from .models import Interaction

from discord.utils import setup_logging

log = getLogger(__name__)

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
        self._components: Dict[str, Component] = {}
        self._app_commands: Dict[str, Union[Group, Command]] = {}
        self.error_handler: Optional[AsyncFunction] = self.on_command_error
        log.info("Ok")
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

    def get_command(self, name: str) -> Union[Command, Group, None]:
        """
        Get a slash command with the specified name.

        Parameters
        ----------
        name : str
            The name of the command to retrieve.

        Returns
        -------
        Union[Command, Group, None]
            The command object with the specified name, or None if no such object exists.
        """
        return self._app_commands.get(name)

    def run(self, **kwargs):
        """
        Starts the web server to handle HTTP interactions with Discord.
        """
        import uvicorn

        kwargs["log_config"] = kwargs.get("log_config", LOGGING_CONFIG)
        uvicorn.run(**kwargs)

    async def _dispatch_callback(self, coro: AsyncFunction, *args, **kwargs):
        """
        Dispatches an event to a single event listener.
        """
        try:
            await coro(*args, **kwargs)
        except Exception as e:
            log.error("An error occured in %s" % coro.__name__, exc_info=e)

    def dispatch(self, event_name: str, *args, **kwargs):
        """
        Dispatches an event to all registered event listeners.

        Parameters
        ----------
        event_name: str
            The name of the event to dispatch.
        *args: Any
            positional arguments to pass to the event listeners.
        **kwargs: Any
            keyword arguments to pass to the event listeners.
        """
        if not event_name.startswith("on_"):
            event_name = "on_" + event_name
        event = self._events.get(event_name)
        if not event:
            return
        for coro in event:
            asyncio.ensure_future(self._dispatch_callback(coro, *args, **kwargs))

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
            >>> app = dismake.Bot(...)
            >>> @app.event()
            ... async def on_ready():
            ...     print(f"Logged in as {app.user}.")
        """

        def decorator(coro: AsyncFunction):
            @wraps(coro)
            def wrapper(*_, **__):
                name = event_name or coro.__name__
                if self._events.get(name) is not None:
                    self._events[name].append(coro)
                else:
                    self._events[name] = [coro]

            return wrapper()

        return decorator

    async def sync_commands(self, guild_ids: Optional[int] = None):
        """
        Synchronizes all application commands to Discord.

        Parameters
        ----------
        guild_ids: Optional[int]:
            An optional list of guild IDs to sync commands for. If not specified, commands will be synced globally.

        Returns
        -------
        A list of the updated application commands on success.

        Example usage
        -------------
            >>> from dismake import Dismake
            >>> app = Dismake()
            >>> @app.command()
            ... async def hello(ctx):
            ...     await ctx.respond("Hello, world!")
            >>> @app.event('ready')
            ... async def on_ready():
            ...     await app.sync_commands()
        """
        return await self._http.bulk_override_commands(
            [command for command in self._app_commands.values()]
        )

    def on_error(self, coro: AsyncFunction):
        """
        A decorator which overrides the `:meth: _default_error_handler`.

        Example usage
        -------------
            >>> import dismake
            >>> app = dismake.Bot(...)
            >>> @app.on_app_command_error
            ... async def custom_error_handler(ctx, error):
            ...     # Your error handler logics
            ...     pass
        """

        @wraps(coro)
        def wrapper(*_, **__):
            self.error_handler = coro
            return coro

        return wrapper()

    async def on_command_error(self, interaction: Interaction, error: Exception) -> Any:
        """
        A default error handler which handles the CommandInvokeError
        """
        if isinstance(error, CommandInvokeError):
            await interaction.respond(
                f"Oops! Something went wrong while running the command.", ephemeral=True
            )
        raise error

    async def fetch_guild(self, guild_id: int) -> Guild:
        """
        Fetches a guild from discord by its ID.

        Parameters
        ----------
        guild_id: int
            The ID of the guild to fetch.

        Returns
        -------
        A Guild object representing the requested guild.

        Raises
        ------
        HTTPStatusError: If the API request fails.
        """
        res = await self._http.client.request(method="GET", url=f"/guilds/{guild_id}")
        res.raise_for_status()
        return Guild(**res.json())

    def add_house(self, house: House) -> None:
        """
        Registers a :class:`~dismake.ui.House` for persistent listening.

        Parameters
        ----------
        house: House
            The House object to register for dispatching.
        """
        if not (components := house.components):
            return
        for component in components:
            if self._components.get((custom_id := component.custom_id)):
                continue
            self._components[custom_id] = component

    def add_command(self, command: Union[Command, Group]):
        """
        The add_command function is used to add a command or group of commands to the application.

        Parameters
        ----------
        command: Union[Command, Group]
            The command you want to add to dismake.Bot
        """
        self._app_commands[command.name] = command

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
        The `command` function is a decorator that registers a function as an application command.

        Parameters
        ----------
        name : str
            The name of the command.
        description : str
            The description of the command.
        guild_id : int | None
            The guild ID, if you want this command to only be visible on a specific guild.
        default_member_permissions : Permissions | None
            The permissions a user needs to invoke this command.
        guild_only : bool | None
            If set to True, this command will only be visible to guilds, not in user DM channels.
        nsfw : bool | None
            If set to True, this command will only be visible in NSFW channels.
        name_localizations : dict[str, str] | None
            Localization dictionary for name field. Values follow the same restrictions as name
        description_localizations : dict[str, str] | None
            Localization dictionary for description field. Values follow the same restrictions as description
        """

        def decorator(coro: AsyncFunction):
            @wraps(coro)
            def wrapper(*_, **__):
                command = Command(
                    name=name if name else coro.__name__,
                    description=description,
                    guild_id=guild_id,
                    callback=coro,
                    nsfw=nsfw,
                    default_member_permissions=default_member_permissions,
                    guild_only=guild_only,
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
    ):
        """
        The create_group function is a helper function that creates a new Group object and adds it to the list of commands.

        Parameters
        ----------
        name: str
            The name of the command.
        description: str
            The description of the command.
        guild_id : int | None
            The guild ID, if you want this command to only be visible on a specific guild.
        default_member_permissions : Permissions | None
            The permissions a user needs to invoke this command.
        guild_only : bool | None
            If set to True, this command will only be visible to guilds, not in user DM channels.
        nsfw : bool | None
            If set to True, this command will only be visible in NSFW channels.
        name_localizations : dict[str, str] | None
            Localization dictionary for name field. Values follow the same restrictions as name
        description_localizations : dict[str, str] | None
            Localization dictionary for description field. Values follow the same restrictions as description
        """
        command = Group(
            name=name,
            description=description,
            guild_id=guild_id,
            name_localizations=name_localizations,
            description_localizations=description_localizations,
            default_member_permissions=default_member_permissions,
            guild_only=guild_only,
            nsfw=nsfw,
        )
        self._app_commands[command.name] = command
        return command
