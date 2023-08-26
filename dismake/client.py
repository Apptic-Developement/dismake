from __future__ import annotations

from typing import Sequence
from dismake.http import HttpClient


__all__: Sequence[str] = ("Client",)


class Client:
    def __init__(self, token: str, application_id: int, public_key: str) -> None:
        self.http: HttpClient = HttpClient(
            token=token, application_id=application_id, public_key=public_key
        )

    async def parse_interactions(self):
        ...
