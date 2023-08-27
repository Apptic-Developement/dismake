from __future__ import annotations

from functools import wraps
from logging import getLogger
from typing import TYPE_CHECKING, Any, Sequence, Tuple

from aiohttp import web

from dismake.client import Client
from dismake.enums import InteractionResponseType, InteractionType

if TYPE_CHECKING:
    from dismake.types import AsyncFunction

log = getLogger(__name__)

__all__: Sequence[str] = ("Bot",)


class Bot(Client):
    __slots__: Tuple[str, ...] = (
        "app",
        "_startup_callbacks",
    )
    def __init__(
        self,
        token: str,
        application_id: int,
        public_key: str,
        route: str = "/interactions",
    ) -> None:
        super().__init__(token, application_id, public_key)
        self.app: web.Application = web.Application()
        self.app.add_routes(
            [web.post(path=route, handler=self.handle_interactions)]
        )
        self._startup_callbacks: Tuple[AsyncFunction, ...] = (self.on_ready,)

    async def on_ready(self) -> Any:
        pass

    def on_startup(self):
        def decorator(func: AsyncFunction):
            @wraps(func)
            def wrapper(*_: Any, **__: Any):
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

    def run(self, *args: Any, **kwargs: Any) -> Any:
        web.run_app(self.app, *args, **kwargs) # type: ignore
