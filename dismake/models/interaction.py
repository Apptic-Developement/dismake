from __future__ import annotations

from typing import Any, List, Optional, TYPE_CHECKING, Union, Dict, TYPE_CHECKING
from pydantic import BaseModel, root_validator

from .user import Member, User
from .guild import Guild
from .role import Role
from .message import Message
from ..enums import InteractionType, InteractionResponseType, MessageFlags
from ..errors import InteractionNotResponded, InteractionResponded
from ..ui import SelectOption
from ..params import handle_send_params, handle_edit_params

if TYPE_CHECKING:
    from ..ui import House
    from ..client import Bot
    from ..types import SnowFlake
    from fastapi import Request


__all__ = (
    "Interaction",
    "ApplicationCommandData",
    "ApplicationCommandOption",
    "ComponentContext",
    "ModalContext",
)


class ResolvedData(BaseModel):
    users: Optional[Dict[str, User]]
    members: Optional[Any]
    channels: Optional[Any]
    roles: Optional[Dict[str, Role]]
    messages: Optional[Any]
    attachments: Optional[Any]


class ApplicationCommandOption(BaseModel):
    name: str
    type: int
    value: Optional[Union[str, int, float, bool, User, Role]]
    options: Optional[List[ApplicationCommandOption]]
    focused: bool = False


class ApplicationCommandData(BaseModel):
    id: SnowFlake
    name: str
    type: int
    resolved: Optional[ResolvedData]
    options: Optional[List[ApplicationCommandOption]]
    guild_id: Optional[SnowFlake]
    target_id: Optional[SnowFlake]


class Interaction(BaseModel):
    request: Request
    is_response_done: bool
    id: SnowFlake
    application_id: SnowFlake
    type: int
    guild_id: Optional[int]
    channel: Optional[Any]
    channel_id: Optional[SnowFlake]
    member: Optional[Member]
    user: Optional[User]
    token: str
    version: int
    message: Optional[Message]
    app_permissions: Optional[str]
    locale: Optional[str]
    guild_locale: Optional[str]

    @root_validator
    def _validate_requests(cls, values):
        if values["message"]:
            values["message"]._request = values["request"]
            print(values["message"]._request)
        return values
        
    @property
    def is_responded(self) -> bool:
        return self.is_response_done

    @property
    def is_application_command(self) -> bool:
        return self.type == InteractionType.APPLICATION_COMMAND.value

    @property
    def is_autocomplete(self) -> bool:
        return self.type == InteractionType.APPLICATION_COMMAND_AUTOCOMPLETE.value

    @property
    def is_modal_submit(self) -> bool:
        return self.type == InteractionType.MODAL_SUBMIT.value

    @property
    def is_ping(self) -> bool:
        return self.type == InteractionType.PING.value

    @property
    def is_component(self) -> bool:
        return self.type == InteractionType.MESSAGE_COMPONENT.value

    @property
    def author(self) -> Union[Member, User]:
        if self.guild_id:
            assert self.member is not None
            return self.member
        assert self.user is not None
        return self.user

    async def fetch_guild(self) -> Guild:
        assert self.guild_id is not None, "Guild id is none."
        return await self.bot.fetch_guild(self.guild_id)

    @property
    def bot(self) -> Bot:
        return self.request.app

    async def respond(
        self,
        content: str,
        *,
        tts: bool = False,
        ephemeral: bool = False,
        house: Optional[House] = None,
    ):
        if self.is_responded:
            raise InteractionResponded(self)

        if house:
            self.bot.add_house(house)
        await self.bot._http.client.request(
            method="POST",
            url=f"/interactions/{self.id}/{self.token}/callback",
            json={
                "type": InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE.value,
                "data": handle_send_params(
                    content=content, tts=tts, ephemeral=ephemeral, house=house
                ),
            },
            headers=self.bot._http.headers,
        )
        self.is_response_done = True

    async def defer(self, thinking: bool = True):
        if self.is_responded:
            raise InteractionResponded(self)
        await self.bot._http.client.request(
            method="POST",
            url=f"/interactions/{self.id}/{self.token}/callback",
            json={
                "type": InteractionResponseType.DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE.value,
                "data": {"flags": MessageFlags.LOADING.value} if not thinking else None,
            },
            headers=self.bot._http.headers,
        )
        self.is_response_done = True

    async def send_followup(
        self,
        content: str,
        *,
        tts: bool = False,
        house: Optional[House] = None,
        ephemeral: bool = False,
    ):
        if not self.respond:
            raise InteractionNotResponded(self)

        if house:
            self.bot.add_house(house)
        return await self.bot._http.client.request(
            method="POST",
            url=f"/webhooks/{self.application_id}/{self.token}",
            json=handle_send_params(
                content=content, tts=tts, house=house, ephemeral=ephemeral
            ),
        )

    async def edit_original_response(
        self, content: str, *, tts: bool = False, house: Optional[House] = None
    ):
        if house:
            self.bot.add_house(house)
        return await self.bot._http.client.request(
            method="PATCH",
            url=f"/webhooks/{self.application_id}/{self.token}/messages/@original",
            json=handle_edit_params(content=content, tts=tts, house=house),
        )

    async def get_original_response(self) -> Message:
        res = await self.bot._http.client.request(
            method="GET",
            url=f"/webhooks/{self.application_id}/{self.token}/messages/@original",
        )
        res.raise_for_status()
        return Message(**res.json())

    async def send(
        self,
        content: str,
        *,
        tts: bool = False,
        house: Optional[House] = None,
        ephemeral: bool = False,
    ):
        if self.is_responded:
            return await self.send_followup(
                content, tts=tts, house=house, ephemeral=ephemeral
            )
        return await self.respond(content, tts=tts, house=house, ephemeral=ephemeral)

    class Config:
        arbitrary_types_allowed = True


class MessageComponentData(BaseModel):
    custom_id: str
    component_type: int
    values: Optional[List[SelectOption]]


class ModalSubmitData(BaseModel):
    custom_id: str
    # components	array of message components	the values submitted by the user


class ComponentContext(Interaction):
    data: Optional[MessageComponentData]

    async def edit_message(
        self, content: str, *, tts: bool = False, house: Optional[House] = None
    ):
        if self.is_responded:
            raise InteractionResponded(self)
        if house:
            self.bot.add_house(house)
        payload = handle_edit_params(content=content, tts=tts, house=house)
        return await self.bot._http.client.request(
            method="POST",
            url=f"/interactions/{self.id}/{self.token}/callback",
            json={
                "type": InteractionResponseType.UPDATE_MESSAGE.value,
                "data": payload,
            },
        )


class ModalContext(Interaction):
    data: Optional[ModalSubmitData]
