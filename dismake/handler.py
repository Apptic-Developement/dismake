from __future__ import annotations

from logging import getLogger
from typing import Any, TYPE_CHECKING
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
from .enums import InteractionType, InteractionResponseType
from .commands import Context
from .models import Interaction
from .ui import ComponentContext
from .errors import CommandInvokeError, NotImplemented
from .app_commands import Command, Group

if TYPE_CHECKING:
    from .client import Bot
log = getLogger("uvicorn")


class InteractionHandler:
    def __init__(self, client: Bot) -> None:
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

    # async def _handle_command(self, request: Request) -> Any:
    #     payload: dict = await request.json()
    #     payload.update({"request": request, "is_response_done": False})
    #     context = Context.parse_obj(payload)
    #     if (data := context.data) is not None:
    #         command = self.client._slash_commands.get(data.name)
    #         if not command:
    #             raise NotImplemented(f"Command {data.name!r} not found.")
    #         try:
    #             await command.before_invoke(context)
    #             await command.callback(context)
    #             await command.after_invoke(context)
    #         except Exception as e:
    #             await self.client._error_handler(
    #                 context, CommandInvokeError(command, e)
    #             )
    async def _handle_command(self, request: Request) -> Any:
        payload: dict = await request.json()
        payload.update({"request": request, "is_response_done": False})
        print(payload)
        context = Context.parse_obj(payload)
        if (data := context.data) is not None:
            command = self.client._app_commands.get(data.name)
            if command is not None:
                if isinstance(command, Command):
                    await command.invoke(context)
                elif isinstance(command, Group):
                    assert data.options is not None, "Invalid data recieved."
                    child_2 = command.commands.get(data.options[0].name)
                    if isinstance(child_2, Group):
                        assert data.options[0].options is not None, "Invalid data recieved."
                        child_3 = child_2.commands.get(data.options[0].options[0].name)
                        assert isinstance(child_3, Command)
                        await child_3.invoke(context)
                    if isinstance(child_2, Command):
                        await child_2.invoke(context)
    async def _handle_autocomplete(self, request: Request) -> Any:
        payload: dict = await request.json()
        payload.update({"request": request, "is_response_done": False})
        context = Context.parse_obj(payload)
        if (data := context.data) is not None:
            if command := self.client.get_command(data.name):
                if choices := await command.autocomplete(context):
                    return JSONResponse(
                        {
                            "type": InteractionResponseType.APPLICATION_COMMAND_AUTOCOMPLETE_RESULT.value,
                            "data": {
                                "choices": [choice.to_dict() for choice in choices]
                            },
                        }
                    )
                return JSONResponse(
                    {
                        "type": InteractionResponseType.APPLICATION_COMMAND_AUTOCOMPLETE_RESULT.value,
                        "data": {"choices": []},
                    }
                )

    async def _handle_message_component(self, request: Request) -> Any:
        payload: dict = await request.json()
        payload.update({"request": request, "is_response_done": False})
        ctx = ComponentContext.parse_obj(payload)
        if data := ctx.data:
            comp = self.client._components.get(data.custom_id)
            if comp:
                await comp.callback(ctx)

    async def handle_interactions(self, request: Request):
        signature = request.headers["X-Signature-Ed25519"]
        timestamp = request.headers["X-Signature-Timestamp"]
        if (
            signature is None
            or timestamp is None
            or not self.verify_key(await request.body(), signature, timestamp)
        ):
            return Response(content="Bad Signature", status_code=401)

        payload: dict = await request.json()
        payload.update({"request": request, "is_response_done": False})
        interaction = Interaction(**payload)
        self.client.dispatch(
            "interaction_create",
            interaction,
            payload=payload,
        )
        if payload["type"] == InteractionType.PING.value:
            return JSONResponse({"type": InteractionResponseType.PONG.value})
        if payload["type"] == InteractionType.APPLICATION_COMMAND.value:
            await self._handle_command(request)
        elif payload["type"] == InteractionType.APPLICATION_COMMAND_AUTOCOMPLETE.value:
            return await self._handle_autocomplete(request)
        elif payload["type"] == InteractionType.MESSAGE_COMPONENT.value:
            await self._handle_message_component(request)

        return JSONResponse({"ack": InteractionResponseType.PONG.value})
