from __future__ import annotations

from typing import Any
from httpx import AsyncClient
from nacl.signing import VerifyKey


__all__ = ("HttpClient",)



class HttpClient:
    def __init__(
        self,
        *,
        token: str,
        client_public_key: str
    ) -> None:
        self.token = token
        self.api_version = 10
        self.verify_key = VerifyKey(
            key=bytes.fromhex(client_public_key)
        )
    
    @property
    def base_url(self) -> str:
        return "https://discord.com/api/v%s/" % self.api_version
    


    @property
    def headers(self) -> dict:
        return {"Authorization": "Bot %s" % self.token}

    async def request(self):
        ...
    async def get(self):
        ...

    async def post(self):
        ...

    async def put(self):
        ...

    async def delete(self):
        ...

