from __future__ import annotations
from typing import List, Optional, Union, TYPE_CHECKING
from logging import getLogger
from httpx import AsyncClient
from .models import User
if TYPE_CHECKING:
    from .commands import Command, Group
    from .models import AppCommand
    from httpx import Response

log = getLogger(__name__)

__all__ = ("HttpClient",)


class HttpClient:
    def __init__(
        self,
        *,
        token: str,
        client_id: int,
    ) -> None:
        self.token = token
        self.client_id = client_id
        self.api_version = 10
        self.app_command_endpoint = f"/applications/{client_id}/commands"
        self.client = AsyncClient(base_url=self.base_url, headers=self.headers)
        self._user: User

    @property
    def base_url(self) -> str:
        return "https://discord.com/api/v%s/" % self.api_version

    @property
    def headers(self) -> dict[str, str]:
        return {"Authorization": "Bot %s" % self.token}

    async def get_global_commands(self) -> list[AppCommand]:
        res = await self.client.request(
            method="GET",
            url=f"/applications/{self.client_id}/commands",
        )
        res.raise_for_status()
        return [AppCommand(**command) for command in res.json()]

    async def bulk_override_commands(
        self, commands: List[Union[Command, Group]], guild_id: Optional[int] = None
    ) -> list[AppCommand]:
        res = await self.client.request(
            method="PUT",
            url=f"/applications/{self.client_id}/commands",
            json=[command.to_dict() for command in commands],
            headers=self.headers,
        )
        res.raise_for_status()
        return [AppCommand.parse_obj(cmd) for cmd in res.json()]

    async def remove_all_commands(self) -> Response:
        res = await self.client.request(
            method="PUT",
            url=f"/applications/{self.client_id}/commands",
            json=[],
        )
        res.raise_for_status()
        return res

    async def fetch_me(self) -> None:
        res = await self.client.request(
            method="GET", url="/users/@me", headers=self.headers
        )
        res.raise_for_status()
        self._user = User(**res.json())
