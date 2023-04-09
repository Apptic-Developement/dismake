from __future__ import annotations
import json

from logging import getLogger
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
from .enums import InteractionType, InteractionResponseType
from ._types import ClientT
from .commands import Context
from .errors import CommandInvokeError, NotImplemented

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
            context = Context(request=request, **_json)
            if (data := context.data) is not None:
                command = self.client._slash_commands.get(data.name)
                if not command: raise NotImplemented(f"Command {data.name!r} not found.")
                try:
                    await command.callback(context)
                except Exception as e:
                    await self.client._error_handler(context, CommandInvokeError(command, e))
        elif (
            request_body["type"]
            == InteractionType.APPLICATION_COMMAND_AUTOCOMPLETE.value
        ):
            interaction = Context(request=request, **_json)
            if (data := interaction.data) is not None:
                command = self.client.get_command(data.name)
                if command:
                    choices = await command.autocomplete(interaction)
                    if choices:
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
        return JSONResponse({"ack": InteractionResponseType.PONG.value})


a = {
    "app_permissions": "70368744177663",
    "application_id": "1071851326234951770",
    "channel": {
        "flags": 0,
        "guild_id": "882441738713718815",
        "id": "1070755073866616865",
        "last_message_id": "1094480851804360724",
        "name": "│chat",
        "nsfw": False,
        "parent_id": "997068127907090442",
        "permissions": "70368744177663",
        "position": 11,
        "rate_limit_per_user": 0,
        "topic": None,
        "type": 0,
    },
    "channel_id": "1070755073866616865",
    "data": {
        "id": "1094476355678245004",
        "name": "autocomplete",
        "options": [
            {
                "name": "fruit",
                "options": [
                    {"name": "your-name", "type": 3, "value": "Pranoy"},
                    {"focused": True, "name": "fav-fruit", "type": 3, "value": ""},
                ],
                "type": 1,
            }
        ],
        "type": 1,
    },
    "entitlement_sku_ids": [],
    "entitlements": [],
    "guild_id": "882441738713718815",
    "guild_locale": "en-US",
    "id": "1094607962556878888",
    "locale": "en-GB",
    "member": {
        "avatar": None,
        "communication_disabled_until": None,
        "deaf": False,
        "flags": 0,
        "is_pending": False,
        "joined_at": "2023-02-02T15:47:56.859000+00:00",
        "mute": False,
        "nick": None,
        "pending": False,
        "permissions": "70368744177663",
        "premium_since": None,
        "roles": ["1070758821573693624", "1071341486702088193", "1071340327287390248"],
        "user": {
            "avatar": "f7f2e9361e8a54ce6e72580ac7b967af",
            "avatar_decoration": None,
            "discriminator": "3299",
            "display_name": None,
            "global_name": None,
            "id": "1070349326884290602",
            "public_flags": 0,
            "username": "Pranoy",
        },
    },
    "token": "aW50ZXJhY3Rpb246MTA5NDYwNzk2MjU1Njg3ODg4ODpvNFNRNFNGTFZCTlY2aVVxNTI1UGFxZ3ZTZlB4dkJlVThUcXY5c0lwMENnRkVMN2ZKMHlVZFF6U0VOTDJEaVR1T2xZMndOYm5MRWp3bTJhY2xpS29PTmZoU202cmxmSXpuRGdHQThWcWh1ZFVZem9IYjF2dmtYQ1NCSFN6c1VPcQ",
    "type": 4,
    "version": 1,
}
