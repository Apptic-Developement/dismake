from __future__ import annotations

import typing
import aiohttp

from yarl import URL

__all__: typing.Sequence[str] = ("HttpClient",)


class HttpClient:
    def __init__(self, token: str, application_id: int) -> None:
        self.token = token
        self.application_id = application_id
        self.session: aiohttp.ClientSession = aiohttp.ClientSession(
            base_url=URL("https://discord.com/api/v/10"),
            headers={"Authorization": f"Bot {token}"},
        )

