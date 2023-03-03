from __future__ import annotations


__all__ = ("HttpClient",)



class HttpClient:
    def __init__(
        self,
        *,
        token: str,
    ) -> None:
        self.token = token
        self.api_version = 10
    
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

