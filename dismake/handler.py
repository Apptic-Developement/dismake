from __future__ import annotations
import json

from logging import getLogger
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
from .enums import CommandType, InteractionType, InteractionResponseType, OptionType
from .interaction import Interaction,CommandData
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
            log.info("Successfully responded to discord.")
            return JSONResponse({"type": InteractionResponseType.PONG.value})


        elif request_body["type"] == InteractionType.APPLICATION_COMMAND.value:
            interaction = Interaction(request=request, **_json)
            assert isinstance(interaction.data, CommandData)
            command = self.client._global_application_commands.get(interaction.data.name)
            if not command:
                raise NotImplemented(
                    f"An unknown command called {interaction.data.name!r} ran by {interaction.member or interaction.user}."
                )
            if interaction.data.type != CommandType.SLASH:
                # TODO: Context Menu
                raise NotImplemented("Context menus are not implimented.")
            elif (
                interaction.data.options
                and len(interaction.data.options) == 1
                and interaction.data.options[0].type
                in (OptionType.SUB_COMMAND, OptionType.SUB_COMMAND_GROUP)
            ):
                if interaction.data.options[0].type == OptionType.SUB_COMMAND:
                    child = command.subcommands.get(interaction.data.options[0].name)
                    if child is None:
                        raise ValueError("Not Impl {command.name} {sub_group.name}")
                    if child and child.callback:
                        await child.callback(interaction)
                else:
                    sub_group = command.subcommands.get(
                        interaction.data.options[0].name
                    )
                    if sub_group is None:
                        raise ValueError(
                            "Not Impl {command.name} {sub_group.name}"
                        )  # TODO:
                    if interaction.data.options[0].options:
                        child = sub_group.subcommands.get(
                            interaction.data.options[0].options[0].name
                        )
                        if child and child.callback:
                            await child.callback(interaction)

            else:
                await command.callback(interaction)
        return JSONResponse({"ack": InteractionResponseType.PONG.value})