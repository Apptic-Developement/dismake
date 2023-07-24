from __future__ import annotations

from typing import TYPE_CHECKING, Any

from fastapi import FastAPI

from .handler import InteractionHandler
from .http import HttpClient
from .commands import Command, Group

if TYPE_CHECKING:
    ...

__all__ = ("Client",)


class Client(FastAPI):
    """
    The base client class for dismake.

    Parameters
    ----------
    token: str
        The token of the bot.
    application_id: int | str
        The application ID of the bot.
    public_key: str
        The public key of the bot.
    route: str
        The route to listen for interactions on.
    **kwargs
        Keyword arguments to pass to the FastAPI instance.
    """

    def __init__(
        self,
        token: str,
        public_key: str,
        application_id: int | str,
        interaction_route: str = "/interaction",
        **kwargs: dict[Any, Any],
    ):
        super().__init__(**kwargs)
        self._token = token
        self._public_key = public_key
        self._application_id = application_id
        self._interaction_route = interaction_route
        self._commands: dict[str, Command | Group] = {}
        self._components: dict[str, Any] = {}

        self._http: HttpClient = HttpClient(
            application_id=self._application_id,
            token=self._token,
            public_key=self._public_key,
        )
        self._interaction_handler = InteractionHandler(client=self)

    @property
    def commands(self) -> list[Command | Group]:
        return list(self._commands.values())

    @property
    def http(self) -> HttpClient:
        return self._http

    @http.setter
    def http(self, value: HttpClient) -> HttpClient:
        self._http = value
        return value

    @property
    def interaction_handler(self) -> InteractionHandler:
        return self._interaction_handler

    @interaction_handler.setter
    def interaction_handler(self, value: InteractionHandler) -> InteractionHandler:
        self._interaction_handler = value
        return value

    @property
    def interaction_route(self) -> str:
        return self._interaction_route

    @interaction_route.setter
    def interaction_route(self, value: str) -> str:
        self._interaction_route = value
        return value
