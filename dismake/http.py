from __future__ import annotations

from typing import  Sequence

from aiohttp import ClientSession
from yarl import URL


__all__: Sequence[str] = ("HttpClient",)


class HttpClient:
    def __init__(self, token: str, application_id: str) -> None:
        self.__token = token
        self.application_id = application_id
        self.session = ClientSession(
            base_url=URL("https://discord.com/api/v/10"),
            headers={"Authorization": f"Bot {token}"},
        )

    # async def fetch_application_commands(
    #     self, guild_id: Optional[str] = None, with_localizations: bool = False
    # ) -> List[ApplicationCommandData]:
    #     if guild_id:
    #         url = f"/applications/{self.application_id}/guilds/{guild_id}/commands?with_localizations={with_localizations}"
    #     else:
    #         url = f"/applications/{self.application_id}/commands?with_localizations={with_localizations}"

    #     res = await self.session.request(method="GET", url=url)
    #     return await res.json()

    # async def bulk_overwrite_application_commands(
    #     self, commands: List[ApplicationCommandData]
    # ) -> List[ApplicationCommandData]:
    #     res = await self.session.put(
    #         url=f"/applications/{self.application_id}/commands", data=[commands]
    #     )

    #     return await res.json()
