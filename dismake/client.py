from __future__ import annotations

import json

from fastapi import FastAPI, Request
from loguru import logger as log
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
from .models import SlashCommand, SubCommand

from .http import HttpClient
from .types import InteractionType, InteractionResponseType


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
        self._slash_commands = {}

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

    def register_slash_command(self, command: SlashCommand):
        pass
    def listen(self, command: SlashCommand):
        def decorator(callback):
            self._slash_commands[command.name] = callback
            print(self._slash_commands)
            print(command.dict(exclude_none=True))
        return decorator
    
    # def listen_for_subcommand(self, command: SubCommand):
    #     def decorator(callback):
    #         self._slash_commands[command.get_name] = callback
    #         print(self._slash_commands)
    #         print(command.dict(exclude_none=True))
    #     return decorator
