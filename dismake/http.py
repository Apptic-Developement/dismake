from __future__ import annotations
from typing import List, Optional, Union
from logging import getLogger
from httpx import AsyncClient, Response

from .commands import Command, Group
from .models import User
from .models import AppCommand

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
    def headers(self) -> dict:
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
    ) -> Response:
        res = await self.client.request(
            method="PUT",
            url=f"/applications/{self.client_id}/commands",
            json=[command.to_dict() for command in commands],
            headers=self.headers,
        )
        res.raise_for_status()
        return res

    async def remove_all_commands(self):
        res =  await self.client.request(
            method="PUT",
            url=f"/applications/{self.client_id}/commands",
            json=[],
        )
        res.raise_for_status()
        return res
    async def fetch_me(self):
        res = await self.client.request(
            method="GET", url="/users/@me", headers=self.headers
        )
        res.raise_for_status()
        self._user = User(**res.json())
