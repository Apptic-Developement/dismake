from __future__ import annotations

from typing import Any, TYPE_CHECKING
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
from .enums import InteractionType, InteractionResponseType
from .models import Interaction, ApplicationCommandData, MessageComponentData
from .app_commands import Command, Group
from loguru import logger as log

if TYPE_CHECKING:
    from .client import Bot


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

    async def _handle_command(self, request: Request) -> Any:
        payload: dict = await request.json()
        interaction = Interaction(request=request, data=payload)
        assert isinstance(interaction.data, ApplicationCommandData)
        if (data := interaction.data) is not None:
            command = self.client._app_commands.get(data.name)
            if command is not None:
                if isinstance(command, Command):
                    await command.invoke(interaction)
                elif isinstance(command, Group):
                    assert data.options is not None, "Invalid data recieved."
                    child_2 = command.commands.get(data.options[0].name)
                    if isinstance(child_2, Group):
                        assert (
                            data.options[0].options is not None
                        ), "Invalid data recieved."
                        child_3 = child_2.commands.get(data.options[0].options[0].name)
                        assert isinstance(
                            child_3, Command
                        ), f"command {child_3} is too nested."
                        await child_3.invoke(interaction)
                    if isinstance(child_2, Command):
                        await child_2.invoke(interaction)

    async def _handle_autocomplete(self, request: Request) -> Any:
        payload: dict = await request.json()
        interaction = Interaction(request=request, data=payload)

        if not (
            interaction.data is not None
            and isinstance(interaction.data, ApplicationCommandData)
            and interaction.is_autocomplete
        ):
            return
        if not (command := self.client.get_command(interaction.data.name)):
            return

        if isinstance(command, Command) and interaction.data.options is not None:
            options = interaction.data.options
            focused = list(filter(lambda x: x.focused == True, options))
            if not focused:
                raise ValueError("No focus items! Probably this is a discord bug.")
            return await command.invoke_autocomplete(interaction, name=focused[0].name)

        if isinstance(command, Group) and interaction.data.options is not None:
            child_2 = command.commands.get(interaction.data.options[0].name)
            if (
                isinstance(child_2, Command)
                and interaction.data.options[0].options is not None
            ):
                options = interaction.data.options[0].options
                focused = list(filter(lambda x: x.focused == True, options))
                if not focused:
                    raise ValueError("No focus items! Probably this is a discord bug.")
                return await child_2.invoke_autocomplete(
                    interaction, name=focused[0].name
                )
            if isinstance(child_2, Group) and interaction.data.options[0].options:
                child_3 = child_2.commands.get(
                    interaction.data.options[0].options[0].name
                )
                if (
                    isinstance(child_3, Command)
                    and interaction.data.options[0].options[0].options is not None
                ):
                    options = interaction.data.options[0].options[0].options
                    focused = list(filter(lambda x: x.focused == True, options))
                    if not focused:
                        raise ValueError(
                            "No focus items! Probably this is a discord bug."
                        )
                    return await child_3.invoke_autocomplete(
                        interaction, name=focused[0].name
                    )

    async def _handle_message_component(self, request: Request) -> Any:
        payload: dict = await request.json()
        interaction = Interaction(request=request, data=payload)
        if interaction.data and isinstance(interaction.data, MessageComponentData):
            comp = self.client._components.get(interaction.data.custom_id)
            if comp:
                return await comp.callback(interaction)

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
        interaction = Interaction(request=request, data=payload)
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
            await self._handle_autocomplete(request)
        elif payload["type"] == InteractionType.MESSAGE_COMPONENT.value:
            await self._handle_message_component(request)

        return JSONResponse({"ack": InteractionResponseType.PONG.value})
