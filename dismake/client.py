# App Commands Reges: ^[-_\p{L}\p{N}\p{sc=Deva}\p{sc=Thai}]{1,32}$
from __future__ import annotations

import json

from fastapi import FastAPI
from dismake.middleware import VerificationMiddleware
from loguru import logger as log




__all__ = ("Client",)


class Client:
    def __init__(
        self, token: str, client_public_key: str, client_id: int, app: FastAPI
    ) -> None:
        self._client_id = client_id
        self._app = app
        self._client_public_key = client_public_key
        self._app.add_middleware(
            VerificationMiddleware,
            client_public_key=self._client_public_key
        )

    # @property
    # def user(self) -> User:
    #     ...

    # def verify_key(self, body: bytes, signature: str, timestamp: str):
    #     message = timestamp.encode() + body
    #     try:
    #         # self.http.verify_key.verify(message, bytes.fromhex(signature))
    #         return True
    #     except Exception as e:
    #         log.error(e)
    #         return False

    # @log.catch
    # async def handle_interactions(self, request: Request):
    #     signature = request.headers["X-Signature-Ed25519"]
    #     timestamp = request.headers["X-Signature-Timestamp"]

    #     if (
    #         signature is None
    #         or timestamp is None
    #         or not self.verify_key(await request.body(), signature, timestamp)
    #     ):
    #         return log.error("Bad request signature")

    #     request_body = json.loads(await request.body())
    #     if request_body["type"] == InteractionType.PING:
    #         return {"type": InteractionResponseType.PONG}
    #     print(request_body)
