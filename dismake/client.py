from __future__ import annotations
import json, logging


from functools import wraps
from typing import Optional
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
from .app_commands.command import Option
from .types import AsyncFunction

from .types import SnowFlake

from .enums import InteractionResponseType, InteractionType
from .api import API
from .models import User, ApplicationCommand
from .app_commands import SlashCommand
from .utils import LOGGING_CONFIG

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
        self.add_event_handler("startup", self._http.fetch_me)
        self.add_event_handler("startup", self._init_commands)
        self._global_application_commands: dict[str, SlashCommand] = {}
        self._queue_global_application_commands: dict[str, SlashCommand] = {}
        self._guild_application_commands: dict[str, SlashCommand] = {}
        self._queue_guild_application_commands: dict[str, SlashCommand] = {}
        self._listeners = {}

    @property
    def user(self) -> User:
        return self._http._user

    def get_command(self, name: str) -> Optional[ApplicationCommand]:
        command = self._global_application_commands[name]
        if not command:
            return None
        return command.partial

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

    async def _init_commands(self):
        log.info("Commands initializing...")
        r_commands = await self._http.get_global_commands()
        if not r_commands:
            log.info("No registered commands found.")
            return
        if not self._queue_global_application_commands:
            log.critical("No commands found.")
            return

        initialized_commands: int = 0
        for rcommand in r_commands:
            for mcommand in self._queue_global_application_commands.values():
                if rcommand.name == mcommand.name:
                    initialized_commands += 1
                    self._global_application_commands[rcommand.name] = mcommand
                    mcommand._partial = rcommand
        log.info(
            f"{initialized_commands} {'command is' if initialized_commands == 1 else 'commands are'} successfully initialized."
        )

    async def sync_commands(self, *, guild_id: Optional[int] = None):
        if not guild_id:
            res = await self._http.bulk_override_commands(
                [
                    command
                    for command in self._queue_global_application_commands.values()
                ]
            )
            await self._init_commands()
            return res.json()

    def run(self, **kwargs):
        import uvicorn
        kwargs["log_config"] = kwargs.get("log_config", LOGGING_CONFIG)
        uvicorn.run(**kwargs)

    def add_command(self, command: SlashCommand):
        if command.guild_id:
            self._queue_guild_application_commands[command.name] = command
            return command
        self._queue_global_application_commands[command.name] = command
        return command

    def add_commands(self, commands: list[SlashCommand]):
        for command in commands:
            if command.guild_id:
                self._queue_guild_application_commands[command.name] = command
            else:
                self._queue_global_application_commands[command.name] = command

    def command(
        self,
        name: str,
        description: str,
        options: Optional[list[Option]] = None,
        guild_id: Optional[SnowFlake] = None,
    ):
        def decorator(coro: AsyncFunction):
            @wraps(coro)
            def wrapper(*_, **__):
                command = SlashCommand(
                    name=name,
                    description=description,
                    guild_id=guild_id,
                    options=options,
                    callback=coro,
                )
                return self.add_command(command)

            return wrapper()

        return decorator
