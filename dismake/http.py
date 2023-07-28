from __future__ import annotations

from typing import TYPE_CHECKING

from httpx import AsyncClient

if TYPE_CHECKING:
    from .commands import Command, Group


__all__ = ("HttpClient",)


class HttpClient:
    """
    The base http class for dismake.

    Parameters
    ----------
    token: str
        The token of the bot.
    application_id: int | str
        The application ID of the bot.
    public_key: str
        The public key of the bot.
    """

    def __init__(self, token: str, public_key: str, application_id: int | str):
        self._token = token
        self._public_key = public_key
        self._application_id = application_id
        self._client = AsyncClient

    @property
    def request(self) -> AsyncClient:
        return AsyncClient()

    async def sync_commands(self, commands: list[Command | Group]) -> list[Command | Group]:
        raise NotImplementedError