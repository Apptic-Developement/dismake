from __future__ import annotations
import json

from logging import getLogger
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
from .enums import CommandType, InteractionType, InteractionResponseType, OptionType
from .interaction import Interaction, CommandInteraction
from ._types import ClientT
from .errors import NotImplemented

log = getLogger("uvicorn")


class InteractionHandler:
    def __init__(self, client: ClientT) -> None:
        self.client = client
        self.verification_key = VerifyKey(bytes.fromhex(client._client_public_key))

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
            return JSONResponse({"type": InteractionResponseType.PONG.value})
        if request_body["type"] == InteractionType.APPLICATION_COMMAND.value:
            interaction = CommandInteraction(request=request, **_json)
            if (data := interaction.data) is not None:
                command = self.client._slash_commands.get(data.name)
                if command:
                    await command.callback(interaction)
        return JSONResponse({"ack": InteractionResponseType.PONG.value})
