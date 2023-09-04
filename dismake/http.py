from __future__ import annotations

from typing import Sequence

from aiohttp import ClientSession
from yarl import URL

__all__: Sequence[str] = ("HttpClient",)


class HttpClient:
    def __init__(self, token: str, application_id: int) -> None:
        self.__token = token
        self.application_id = application_id
        self.session = ClientSession(
            base_url=URL("https://discord.com/api/v/10"),
            headers={"Authorization": f"Bot {token}"},
        )
