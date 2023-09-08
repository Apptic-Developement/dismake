from __future__ import annotations


from logging import getLogger, INFO
from typing import TYPE_CHECKING, Any, Sequence, Tuple

from aiohttp import web

from .client import Client
from .enums import InteractionResponseType, InteractionType
from .utils import setup_logging

if TYPE_CHECKING:
    from .client import Client
    from .types import InteractionData

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
        application_id: str,
        public_key: str,
        route: str = "/interactions",
    ) -> None:
        super().__init__(token, application_id, public_key)
        self.app = web.Application()
        self.app.add_routes([web.post(path=route, handler=self.handle_interactions)])
        self.route = route

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
            log.error("Bad signature.")
            return web.json_response({"message": "Invalid interaction."})

        body: InteractionData = await request.json()

        if body["type"] == InteractionType.PING.value:
            return web.json_response({"type": InteractionResponseType.PONG.value})

        await self.parse_interaction_create(body)
        return web.json_response({"ack": InteractionResponseType.PONG.value})

    def run(self, *args: Any, **kwargs: Any) -> Any:
        setup_logging(INFO)
        if kwargs.get("print") is None:

            def _start_callback(x: str) -> None:
                url: str = x[19:-32]
                log.info(f"Server running on: {url}")
                log.info(f"Interaction url: {url}{self.route}")

            kwargs["print"] = _start_callback

        web.run_app(self.app, *args, **kwargs)  # ... # type: ignore
