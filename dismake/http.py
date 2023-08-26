from __future__ import annotations

from typing import TYPE_CHECKING, Literal, Sequence
from aiohttp import ClientSession

if TYPE_CHECKING:
    from aiohttp.typedefs import StrOrURL

__all__: Sequence[str] = ("HttpClient",)


class HttpClient:
    def __init__(self, token: str, application_id: int, public_key: str) -> None:
        self.token = token
        self.application_id = application_id
        self.public_key = public_key
        self.session: ClientSession = ClientSession()

    async def request(
        self, method: Literal["GET", "PUT", "PATCH", "POST", "DELETE"], route: StrOrURL
    ):
        return await self.session.request(method=method, url=route)
