from __future__ import annotations
from typing import Literal, Optional

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

    @property
    def base_url(self) -> str:
        return "https://discord.com/api/v%s/" % self.api_version

    @property
    def headers(self) -> dict:
        return {"Authorization": "Bot %s" % self.token}

    async def register_command(self, command: SlashCommand) -> Optional[bool]:
        res = await self.post(
            route=self.app_command_endpoint,
            payload=command.to_dict()
        )
        if res.status_code == 200:
            return True
        
        res.raise_for_status()


    async def delete_command(self, command: SlashCommand) -> Optional[bool]:
        res = await self.delete(
            route=f"/applications/{self.client_id}/commands/{command._name}",
        )
        if res.status_code == 200:
            return True
        
        res.raise_for_status()


    async def get(self, route: str):
        async with AsyncClient() as client:
            return await client.get(
                url=f"{self.base_url}{route}", headers=self.headers
            )

    async def post(self, route: str, payload: dict):
        async with AsyncClient() as client:
            return await client.post(
                url=f"{self.base_url}{route}", json=payload, headers=self.headers
            )

    async def put(self, route: str, payload: dict | list):
        async with AsyncClient() as client:
            return await client.put(url=f"{self.base_url}{route}", json=payload)

    async def delete(self, route: str):
        async with AsyncClient() as client:
            return await client.delete(
                url=f"{self.base_url}{route}", headers=self.headers
            )