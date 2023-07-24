from __future__ import annotations
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .client import Client
    from fastapi import Request
#     from .commands import Command, Group

__all__ = ("InteractionHandler",)


class InteractionHandler:
    def __init__(self, client: Client) -> None:
        self.client = client
        client.add_api_route(client.interaction_route, self.handle_interactions)

    async def handle_commands(self, request: Request) -> Any:
        raise NotImplementedError

    async def handle_interactions(self, request: Request) -> Any:
        ...
