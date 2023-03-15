from __future__ import annotations
from functools import wraps

import json, logging
from typing import Optional

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
from dismake.app_commands.command import Option
from dismake.types import AsyncFunction

from dismake.types.snowflake import SnowFlake

from .enums import InteractionResponseType, InteractionType
from .api import API
from .models import User
from .app_commands import SlashCommand

log = logging.getLogger("uvicorn")

__all__ = ("Bot",)


class Bot(FastAPI):
    def __init__(
        self,
        token: str,
        client_public_key: str,
        client_id: int,
        route: str = "/interactions",
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self._client_id = client_id
        self._client_public_key = client_public_key
        self.verification_key = VerifyKey(bytes.fromhex(self._client_public_key))
        self._http = API(token=token, client_id=client_id)
        self.add_route(
            path=route,
            route=self.handle_interactions,
            methods=["POST"],
            include_in_schema=False,
        )
        # self.add_event_handler("startup", self._init)
        self.add_event_handler("startup", self._http.fetch_me)

        self._global_application_commands: dict[str, SlashCommand] = {}  # TODO
        self._guild_application_commands: dict[str, SlashCommand] = {}  # TODO

        self._listeners = {}

    @property
    def user(self) -> User:
        return self._http._user

    def verify_key(self, body: bytes, signature: str, timestamp: str):
        message = timestamp.encode() + body
        try:
            self.verification_key.verify(message, bytes.fromhex(signature))
            return True
        except BadSignatureError as e:
            log.error("Bad signature request.")
        except Exception as e:
            log.exception(e)
            return False

    async def handle_interactions(self, request: Request):
        signature = request.headers["X-Signature-Ed25519"]
        timestamp = request.headers["X-Signature-Timestamp"]
        if (
            signature is None
            or timestamp is None
            or not self.verify_key(await request.body(), signature, timestamp)
        ):
            return Response(content="Bad Signature", status_code=401)

        request_body = json.loads(await request.body())
        _json = await request.json()
        if request_body["type"] == InteractionType.PING.value:
            log.info("Successfully responded to discord.")
            return JSONResponse({"type": InteractionResponseType.PONG.value})
        elif request_body["type"] == InteractionType.APPLICATION_COMMAND.value:
            pass

        return JSONResponse({"ack": InteractionResponseType.PONG.value})

    # async def sync_commands(self, *, guild_id: Optional[int] = None):
    #     if not guild_id:
    #         res = await self._http.bulk_override_commands(
    #             [command for _, command in self._slash_commands.items()]
    #         )
    #         return res.json()

    def run(self, **kwargs):
        import uvicorn

        uvicorn.run(**kwargs)

    def add_command(self, command: SlashCommand):
        if command._guild_id:
            self._guild_application_commands[command._name] = command
            return command
        self._global_application_commands[command._name] = command
        return command

    def command(
        self,
        name: str,
        description: str,
        options: Optional[list[Option]] = None,
        guild_id: Optional[SnowFlake] = None,
    ):
        command = SlashCommand(
            name=name, description=description, guild_id=guild_id, options=options
        )

        def decorator(coro: AsyncFunction):
            @wraps(coro)
            def wrapper(*_, **__):
                command._callback = coro
                return self.add_command(command)

            return wrapper()

        return decorator
