from __future__ import annotations
from typing import Optional


from .command import SlashCommand
from httpx import AsyncClient, Response

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
        self.client = AsyncClient(base_url=self.base_url)

    @property
    def base_url(self) -> str:
        return "https://discord.com/api/v%s/" % self.api_version

    @property
    def headers(self) -> dict:
        return {"Authorization": "Bot %s" % self.token}

    async def register_command(self, command: SlashCommand):
        return await self.client.request(
            method="POST",
            url="/applications/%s/commands" % self.client_id,
            json=command.to_dict(),
            headers=self.headers,
        )

    async def get_global_commands(self, only_names: bool = False) -> Optional[dict]:
        res = await self.client.request(
            method="GET",
            url=f"/applications/{self.client_id}/commands",
            headers=self.headers
        )

        _json = res.json()
        if not _json:
            return
        if only_names:
            _names = [command["name"] for command in _json]
            print(_names)
        return _json

    async def remove_all_commands(self):
        return await self.client.request(
            method="PUT",
            url=f"/applications/{self.client_id}/commands",
            headers=self.headers,
            json=[]
        )