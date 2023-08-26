from __future__ import annotations
from functools import wraps

import typing
import logging

from dismake.enums import InteractionResponseType, InteractionType
from dismake.client import Client
from aiohttp import web

from dismake.types import AsyncFunction

if typing.TYPE_CHECKING:
    ...

log = logging.getLogger(__name__)
__all__: typing.Sequence[str] = ("Bot",)


class Bot(Client):
    def __init__(self, token: str, application_id: int, public_key: str) -> None:
        super().__init__(token, application_id, public_key)
        self.app: web.Application = web.Application()
        self.app.add_routes(
            [web.post(path="/interactions", handler=self.handle_interactions)]
        )
        self._startup_callbacks: tuple[AsyncFunction, ...] = (self.on_ready,)

    async def on_ready(self) -> typing.Any:
        pass

    def on_startup(self):
        def decorator(func: AsyncFunction):
            @wraps(func)
            def wrapper(*_: typing.Any, **__: typing.Any):
                self._startup_callbacks = self._startup_callbacks + (func,)
                return func

            return wrapper()

        return decorator

    async def handle_interactions(self, request: web.Request) -> web.Response:
        timestamp = request.headers.get("X-Signature-Timestamp")
        signature = request.headers.get("X-Signature-Ed25519")
        if (
            timestamp
            and signature
            and not self.verify(
                signature=signature, timestamp=timestamp, body=await request.read()
            )
        ):
            log.error("Invalid interaction.")
            return web.json_response({"message": "Invalid interaction."})

        body = await request.json()

        if body["type"] == InteractionType.PING.value:
            return web.json_response({"type": InteractionResponseType.PONG.value})

        await self.parse_interactions(await request.json())
        return web.json_response({"ack": InteractionResponseType.PONG.value})

    def run(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Any:
        web.run_app(self.app, *args, **kwargs)  # type: ignore
