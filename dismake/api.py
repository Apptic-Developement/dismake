from __future__ import annotations
from typing import Optional
from httpx import AsyncClient, Response

from .models import User
from .models import ApplicationCommand


__all__ = ("API",)


class API:
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
        self._user: User

    @property
    def base_url(self) -> str:
        return "https://discord.com/api/v%s/" % self.api_version

    @property
    def headers(self) -> dict:
        return {"Authorization": "Bot %s" % self.token}

    # async def register_command(self, command: SlashCommand):
    #     return await self.client.request(
    #         method="POST",
    #         url="/applications/%s/commands" % self.client_id,
    #         json=command.to_dict(),
    #         headers=self.headers,
    #     )

    async def get_global_commands(self) -> Optional[list[ApplicationCommand]]:
        res = await self.client.request(
            method="GET",
            url=f"/applications/{self.client_id}/commands",
            headers=self.headers,
        )
        res.raise_for_status()
        _json = res.json()
        if not _json:
            return

        return [ApplicationCommand(**command) for command in _json]

    # async def bulk_override_commands(
    #     self, commands: list[SlashCommand], guild_id: Optional[int] = None
    # ) -> Response:
    #     return await self.client.request(
    #         method="PUT",
    #         url=f"/applications/{self.client_id}/commands",
    #         json=[command.to_dict() for command in commands],
    #         headers=self.headers,
    #     )

    async def remove_all_commands(self):
        return await self.client.request(
            method="PUT",
            url=f"/applications/{self.client_id}/commands",
            headers=self.headers,
            json=[],
        )

    async def fetch_me(self):
        res = await self.client.request(
            method="GET", url="/users/@me", headers=self.headers
        )
        res.raise_for_status()
        self._user = User(**res.json())
