from __future__ import annotations

from typing import TYPE_CHECKING, Any, Sequence, Tuple
from logging import getLogger

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
        route: str = "/interactions",
        *args: Any,
        **kwargs: Any
    ) -> None:
        super().__init__(*args, **kwargs)
        self.app: web.Application = web.Application()
        self.app.add_routes([web.post(path=route, handler=self.handle_interactions)])
        self.route = route

    async def on_ready(self) -> Any:
        pass

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

        if body['type'] == InteractionType.PING.value:
            return web.json_response({"type": InteractionResponseType.PONG.value})

        await self.parse_interaction_create(body)
        return web.json_response({"ack": InteractionResponseType.PONG.value})

    def run(self, *args: Any, **kwargs: Any) -> Any:
        setup_logging()
        if kwargs.get("print") is None:

            def _start_callback(x: str) -> None:
                url: str = x[19:-32]
                with open("dismake/banner.txt", "r") as file:
                    banner = file.read()
                print(f"\n\033[94m{banner}\033[0m\n")
                details = {
                    "author": "Pranoy",
                    "email": "officialpranoy2@gmail.com",
                    "docs": "https://dismake.pages.dev/",
                    "support": "https://dismake.pages.dev/support\n",
                }

                reset_color = "\033[0m"

                max_key_length = max(len(key) for key in details.keys())

                for key, value in details.items():
                    spacing = " " * (max_key_length - len(key))
                    print(f"\033[96m{key}:{reset_color}{spacing} {value}")
                log.info(f"Server running on: {url}")
                log.info(f"Interaction url: {url}{self.route}")

            kwargs["print"] = _start_callback
        web.run_app(self.app, *args, **kwargs)  # mypy: ignore # type:ignore
