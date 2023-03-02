# App Commands Reges: ^[-_\p{L}\p{N}\p{sc=Deva}\p{sc=Thai}]{1,32}$
from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from loguru import logger as log


from .http import HttpClient
from .types import InteractionType, InteractionResponseType


__all__ = ("Client",)


class Client:
    def __init__(
        self, token: str, client_public_key: str, client_id: int, app: FastAPI
    ) -> None:
        self.http = HttpClient(token=token, client_public_key=client_public_key)
        self._client_id = client_id
        self._app = app

    # @property
    # def user(self) -> User:
    #     ...

    def verify_key(self, body: bytes, signature: str, timestamp: str):
        message = timestamp.encode() + body
        try:
            self.http.verify_key.verify(message, bytes.fromhex(signature))
        except Exception as e:
            log.error(e)
            return False
        else:
            return True

    @log.catch
    async def handle_interactions(self, request: Request):
        signature = request.headers["X-Signature-Ed25519"]
        timestamp = request.headers["X-Signature-Timestamp"]
        if signature is None or not self.verify_key(await request.body(), signature, timestamp):
            return log.error("Bad request signature")
