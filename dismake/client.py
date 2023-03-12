from __future__ import annotations

import json
import logging
from typing import Optional

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
from dismake.types.command import OptionType
from .command import SlashCommand, Option
from functools import wraps
from .api import API
from .types import (
    AsyncFunction,
    InteractionType,
    InteractionResponseType,
)
from .models import User
from .interaction import Interaction
from .models import Interaction as InteractionData

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
        self._slash_commands: dict[str, SlashCommand] = {}
        self.add_route(
            path=route,
            route=self.handle_interactions,
            methods=["POST"],
            include_in_schema=False,
        )
        self.add_event_handler("startup", self._init)
        self.add_event_handler("startup", self._http.fetch_me)

    @property
    def user(self) -> User:
        return self._http._user

    @property
    def get_commands(self) -> Optional[list[SlashCommand]]:
        if self._slash_commands:
            return list(command for _, command in self._slash_commands.items())

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
        print(_json)
        if request_body["type"] == InteractionType.PING:
            log.info("Successfully responded to discord.")
            return JSONResponse({"type": InteractionResponseType.PONG})
        elif request_body["type"] == InteractionType.APPLICATION_COMMAND:
            interaction = Interaction._from_app_command(
                request, InteractionData(**_json)
            )
            for name, command in self._slash_commands.items():
                if name == _json["data"]["name"]:
                    if command._callback:
                        await command._callback(interaction)
        return JSONResponse({"type": InteractionResponseType.PONG})

    def command(
        self,
        name: str,
        description: Optional[str],
        options: Optional[list[Option]] = None,
    ):
        if name in self._slash_commands.keys():
            raise ValueError(
                f"{name!r} already registered as a slash command please use a different name."
            )

        command = SlashCommand(name=name, description=description)
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

    async def _init(self):
        registered_commands = await self._http.get_global_commands()
        if self._slash_commands:
            if registered_commands:
                for name, command in self._slash_commands.items():
                    for registered_command in registered_commands:
                        if name == registered_command.name:
                            command.id = registered_command.id

    async def sync_commands(self, *, guild_id: Optional[int] = None):
        if not guild_id:
            res = await self._http.bulk_override_commands(
                [command for _, command in self._slash_commands.items()]
            )
            return res.json()


make = {
    "app_permissions": "4398046511103",
    "application_id": "1071851326234951770",
    "channel_id": "1050631408693030973",
    "data": {"id": "1084106102708375653", "name": "ping", "type": 1},
    "entitlement_sku_ids": [],
    "guild_id": "1047495912089473054",
    "guild_locale": "en-US",
    "id": "1084335298739183716",
    "locale": "en-GB",
    "member": {
        "avatar": None,
        "communication_disabled_until": None,
        "deaf": False,
        "flags": 0,
        "is_pending": False,
        "joined_at": "2022-11-30T12:54:47.035000+00:00",
        "mute": False,
        "nick": None,
        "pending": False,
        "permissions": "4398046511103",
        "premium_since": None,
        "roles": [
            "1057154747339128902",
            "1057154942281982055",
            "1057154857166979082",
            "1057154822266179695",
            "1057154622776688720",
            "1057154666250641488",
            "1057154900716441743",
            "1057154978457866291",
            "1047852687405895700",
            "1066238596190834708",
            "1057154781145215038",
            "1057154715193983007",
        ],
        "user": {
            "avatar": "94de12ce96deb607397ade18d6989ed2",
            "avatar_decoration": None,
            "discriminator": "0140",
            "display_name": None,
            "id": "942683245106065448",
            "public_flags": 4194560,
            "username": "Pranoy",
        },
    },
    "token": "aW50ZXJhY3Rpb246MTA4NDMzNTI5ODczOTE4MzcxNjpnSFg5UnFOVXRwRHBmQjZkeFFRNUI3Z1E4dFdEWVFNVUNER0R0eGNhWDIwM0FJY0NXb1gzZDg1VjFLQm1nY0huVHZrNnBpVUFiRnQ2bDBHZGUwVWV3aExtWVlaSGloYWlReldkdk94WmMzaFZuMXB0NllBTHZzcERLZmpyWXF2aw",
    "type": 2,
    "version": 1,
}
