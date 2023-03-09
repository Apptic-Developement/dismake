from __future__ import annotations

import json, asyncio
from typing import Optional

from fastapi import FastAPI, Request
from loguru import logger as log
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

from dismake.types.command import OptionType
from .command import SlashCommand, Option
from functools import wraps

from .http import HttpClient
from .types import (
    AsyncFunction,
    InteractionType,
    InteractionResponseType,
)


__all__ = ("Client",)


class Client:
    def __init__(
        self, token: str, client_public_key: str, client_id: int, app: FastAPI
    ) -> None:
        self._client_id = client_id
        self._app = app
        self._client_public_key = client_public_key
        self.verification_key = VerifyKey(bytes.fromhex(self._client_public_key))
        self._http = HttpClient(token=token)
        self._slash_commands: dict[str, SlashCommand] = {}

    # @property
    # def user(self) -> User:
    #     ...

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
            return

        request_body = json.loads(await request.body())
        if request_body["type"] == InteractionType.PING:
            log.success("Successfully responded to discord.")
            return {"type": InteractionResponseType.PONG}

    def command(
        self,
        name: str,
        description: Optional[str],
        options: Optional[list[Option]] = None,
        guild_id: Optional[int] = None,
    ):
        if name in self._slash_commands.keys():
            raise ValueError(
                f"{name!r} already registered as a slash command please use a different name."
            )

        command = SlashCommand(name=name, description=description, guild_id=guild_id)
        if options:
            for option in options:
                if (
                    option._type != OptionType.SUB_COMMAND
                    or option._type != OptionType.SUB_COMMAND_GROUP
                ):
                    command._options.append(option)

        def decorator(coro: AsyncFunction):
            @wraps(coro)
            def wrapper(*args, **kwargs):
                command.callback = coro
                self._slash_commands[command._name] = command
                return command

            return wrapper()

        return decorator


