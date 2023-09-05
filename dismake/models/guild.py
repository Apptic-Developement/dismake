from __future__ import annotations

from typing import TYPE_CHECKING, Sequence

if TYPE_CHECKING:
    from ..client import Client

__all__: Sequence[str] = ("PartialGuild",)


class PartialGuild:
    def __init__(self, client: Client, id: int) -> None:
        self.client = client
        self.id = id
