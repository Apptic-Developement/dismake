from __future__ import annotations

from fastapi import FastAPI

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
        route: str = "/interaction",
    ):
        self._token = token
        self._public_key = public_key
        self._application_id = application_id
        self._route = route
