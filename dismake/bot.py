from __future__ import annotations

from typing import TYPE_CHECKING, Sequence

from aiohttp.web import Application
from dismake.client import Client

if TYPE_CHECKING:
    ...

__all__: Sequence[str] = ("Bot",)


class Bot(Client):
    def __init__(self, token: str, application_id: int, public_key: str) -> None:
        super().__init__(token, application_id, public_key)
        self.app: Application = Application()
