from __future__ import annotations
import asyncio

from logging import getLogger
from functools import wraps
from typing import Any, Callable, List, Dict, Optional, TYPE_CHECKING
from fastapi import FastAPI
from .handler import InteractionHandler
from .types import AsyncFunction, SnowFlake
from .http import HttpClient
from .models import User
from .utils import LOGGING_CONFIG
from .commands import SlashCommand
from .errors import (
    CommandInvokeError,
    NotImplemented,
    DismakeException
)
if TYPE_CHECKING:
    from .commands import Context
log = getLogger("uvicorn")


__all__ = ("Bot",)


class Bot(FastAPI):
    def __init__(
        self,
        token: str,
        client_public_key: str,
        client_id: int,
        route: str = "/interactions",
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self._client_id = client_id
        self._client_public_key = client_public_key
        self._interaction_handler = InteractionHandler(self)
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
        self._error_handler: AsyncFunction = self._default_error_handler

    @property
    def user(self) -> User:
        return self._http._user

    def get_command(self, name: str) -> Optional[SlashCommand]:
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
        if not guild_ids:
            await self._http.bulk_override_commands(
                [command for command in self._slash_commands.values()]
            )

    def on_app_command_error(self, coro: AsyncFunction):
        @wraps(coro)
        def wrapper(*_, **__):
            self._error_handler = coro
            return coro
        return wrapper()

    async def _default_error_handler(self, ctx: Context, error: Exception) -> Any:
        log.exception(error)
        if isinstance(error, CommandInvokeError):
            return await ctx.respond(f"An error occured.", ephemeral=True)
            
        
