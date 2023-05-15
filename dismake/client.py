from __future__ import annotations
import asyncio
from functools import wraps
from typing import Any, List, Dict, Optional, TYPE_CHECKING, Union
from fastapi import FastAPI
from .models import Guild
from .handler import InteractionHandler
from .http import HttpClient
from .models import User
from .errors import CommandInvokeError
from .commands import Command, Group
from logging import getLogger
from .utils import LOGGING_CONFIG

if TYPE_CHECKING:
    from .ui import View, Component, Modal
    from .types import AsyncFunction
    from .permissions import Permissions
    from .models import Interaction


log = getLogger("dismake")
__all__ = ("Bot",)


class Bot(FastAPI):
    """
    Represents a Discord bot.

    This class is a subclass of `FastAPI`, which means you can create API routes
    and do whatever you can do with `FastAPI`with this class's instance.

    Parameters
    ----------
    token: :class:`str`
        The token for the Discord bot.
    client_public_key: :class:`str`
        The public key for the Discord client.
    client_id: :class:`int`
        The ID for the Discord client.
    route: :class:`str`
        The route to listen for Discord interactions on, by default "/interactions".
    interaction_handler: :class:`InteractionHandler`
        An interaction handler to process incoming Discord interactions, by default :class:`InteractionHandler`.

    Attributes
    ----------
    user: :class:`User`
        The user within this bot.
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
        self._commands: Dict[str, Union[Group, Command]] = {}
        self._modals: Dict[str, Modal] = {}
        self.error_handler: Optional[AsyncFunction] = None
        self.log = log

    @property
    def user(self) -> User:
        """
        Returns the user object representing the bot.

        This property returns a `User` object that represents the bot in the Discord API.

        Returns
        -------
        user: :class:`User`
            The `User` object representing the bot.
        """
        return self._http._user

    def get_command(self, name: str) -> Optional[Union[Command, Group]]:
        """
        Returns the slash command with the specified name, or None if it doesn't exist.

        Parameters
        ----------
        name: str
            The name of the command to retrieve.

        Returns
        -------
        command: Optional[Union[:class:`Command`, :class:`Group`]]
            The command object with the specified name, or None if no such object exists.
        """
        return self._commands.get(name)

    def run(self, **kwargs):
        """
        Starts the web server to handle HTTP interactions with Discord.

        This method starts a web server using `uvicorn`, which handles HTTP interactions with Discord.
        Any additional keyword arguments are passed directly to `uvicorn.run()`.
        By default, this method uses the `LOGGING_CONFIG` configuration for logging,
        but you can provide your own configuration using the `log_config` keyword argument.
        """
        import uvicorn

        kwargs["log_config"] = kwargs.get("log_config", LOGGING_CONFIG)
        uvicorn.run(**kwargs)

    async def _dispatch_callback(self, coro: AsyncFunction, *args, **kwargs):
        """
        Dispatches an event to a single event listener.

        This method is used internally to dispatch an event to a single event listener.
        It calls the specified coroutine function with the given arguments and keyword arguments.
        If the coroutine raises an exception, the exception is logged using the `log` module's `error()` method.

        Parameters
        ----------
        coro:
            The coroutine function to call.
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
        event_name: :class:`str`
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
        guild_ids: Optional[int]
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
            [command for command in self._commands.values()]
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
            await interaction.send(
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

    def add_view(self, view: View) -> None:
        """
        Registers a :class:`~dismake.ui.View` for persistent listening.

        Parameters
        ----------
        view: :class:`View`
            The view object to register for dispatching.
        """
        components = list()
        for row in view.rows:
            for component in row.components:
                components.append(component)

        if not components:
            return
        for component in components:
            if self._components.get((custom_id := component.custom_id)):
                continue
            self._components[custom_id] = component

    def add_modal(self, modal: Modal) -> None:
        """
        Registers a :class:`dismake.ui.Modal` for presistent listening.

        Parameters
        ----------
        modal: :class:`Modal`
            The modal object to register for dispatching.
        """
        self._modals[modal.custom_id] = modal

    def add_command(self, command: Union[Command, Group]):
        """
        The add_command function is used to add a command or group of commands to the application.

        Parameters
        ----------
        command: Union[Command, Group]
            The command you want to add to dismake.Bot
        """
        self._commands[command.name] = command

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
                self._commands[command.name] = command

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
        self._commands[command.name] = command
        return command
