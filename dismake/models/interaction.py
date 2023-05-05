from __future__ import annotations

from typing import Any, List, Optional, TYPE_CHECKING, Union, Dict, TYPE_CHECKING
from pydantic import BaseModel, root_validator
from .user import Member, User
from .guild import Guild
from .role import Role
from .message import Message
from ..enums import InteractionType, InteractionResponseType, MessageFlags, OptionType
from ..errors import InteractionNotResponded, InteractionResponded
from ..params import handle_send_params, handle_edit_params
from fastapi import Request
from ..types import SnowFlake

if TYPE_CHECKING:
    from ..ui import House
    from ..client import Bot


__all__ = (
    "Interaction",
    "ApplicationCommandData",
    "ApplicationCommandOption",
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


# class Interaction(BaseModel):
#     request: Request
#     is_response_done: bool
#     id: SnowFlake
#     application_id: SnowFlake
#     type: int
#     guild_id: Optional[int]
#     channel: Optional[Any]
#     channel_id: Optional[SnowFlake]
#     member: Optional[Member]
#     user: Optional[User]
#     token: str
#     version: int
#     message: Optional[Message]
#     app_permissions: Optional[str]
#     locale: Optional[str]
#     guild_locale: Optional[str]

#     @root_validator
#     def _validate_requests(cls, values):
#         if values["message"]:
#             values["message"]._request = values["request"]
#         return values

#     @property
#     def is_responded(self) -> bool:
#         return self.is_response_done

#     @property
#     def is_application_command(self) -> bool:
#         """
#         The is_application_command function checks if the interaction type is an application command.
#         """
#         return self.type == InteractionType.APPLICATION_COMMAND.value

#     @property
#     def is_autocomplete(self) -> bool:
#         return self.type == InteractionType.APPLICATION_COMMAND_AUTOCOMPLETE.value

#     @property
#     def is_modal_submit(self) -> bool:
#         return self.type == InteractionType.MODAL_SUBMIT.value

#     @property
#     def is_ping(self) -> bool:
#         return self.type == InteractionType.PING.value

#     @property
#     def is_component(self) -> bool:
#         return self.type == InteractionType.MESSAGE_COMPONENT.value

#     @property
#     def author(self) -> Union[Member, User]:
#         if self.guild_id:
#             assert self.member is not None
#             return self.member
#         assert self.user is not None
#         return self.user

#     async def fetch_guild(self) -> Guild:
#         assert self.guild_id is not None, "Guild id is none."
#         return await self.bot.fetch_guild(self.guild_id)

#     @property
#     def bot(self) -> Bot:
#         return self.request.app

#     async def respond(
#         self,
#         content: str,
#         *,
#         tts: bool = False,
#         ephemeral: bool = False,
#         house: Optional[House] = None,
#     ):
#         if self.is_responded:
#             raise InteractionResponded(self)

#         if house:
#             self.bot.add_house(house)
#         await self.bot._http.client.request(
#             method="POST",
#             url=f"/interactions/{self.id}/{self.token}/callback",
#             json={
#                 "type": InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE.value,
#                 "data": handle_send_params(
#                     content=content, tts=tts, ephemeral=ephemeral, house=house
#                 ),
#             },
#             headers=self.bot._http.headers,
#         )
#         self.is_response_done = True

#     async def defer(self, thinking: bool = True):
#         if self.is_responded:
#             raise InteractionResponded(self)
#         await self.bot._http.client.request(
#             method="POST",
#             url=f"/interactions/{self.id}/{self.token}/callback",
#             json={
#                 "type": InteractionResponseType.DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE.value,
#                 "data": {"flags": MessageFlags.LOADING.value} if not thinking else None,
#             },
#             headers=self.bot._http.headers,
#         )
#         self.is_response_done = True

#     async def send_followup(
#         self,
#         content: str,
#         *,
#         tts: bool = False,
#         house: Optional[House] = None,
#         ephemeral: bool = False,
#     ):
#         if self.is_responded != False:
#             raise InteractionNotResponded(self)

#         if house:
#             self.bot.add_house(house)
#         return await self.bot._http.client.request(
#             method="POST",
#             url=f"/webhooks/{self.application_id}/{self.token}",
#             json=handle_send_params(
#                 content=content, tts=tts, house=house, ephemeral=ephemeral
#             ),
#         )

#     async def edit_original_response(
#         self, content: str, *, tts: bool = False, house: Optional[House] = None
#     ):
#         if house:
#             self.bot.add_house(house)
#         return await self.bot._http.client.request(
#             method="PATCH",
#             url=f"/webhooks/{self.application_id}/{self.token}/messages/@original",
#             json=handle_edit_params(content=content, tts=tts, house=house),
#         )

#     async def get_original_response(self) -> Message:
#         res = await self.bot._http.client.request(
#             method="GET",
#             url=f"/webhooks/{self.application_id}/{self.token}/messages/@original",
#         )
#         res.raise_for_status()
#         return Message(**res.json())

#     async def send(
#         self,
#         content: str,
#         *,
#         tts: bool = False,
#         house: Optional[House] = None,
#         ephemeral: bool = False,
#     ):
#         if self.is_responded:
#             return await self.send_followup(
#                 content, tts=tts, house=house, ephemeral=ephemeral
#             )
#         return await self.respond(content, tts=tts, house=house, ephemeral=ephemeral)

#     class Config:
#         arbitrary_types_allowed = True


class Interaction:
    def __init__(self, request: Request, data: Dict[str, Any]) -> None:
        self._request = request
        self._is_response_done = False
        self.id: int = int(data["id"])
        self.application_id: SnowFlake = data["application_id"]
        self.type: int = data["type"]
        self.token: str = data["token"]
        self.version: int = data["version"]
        self.guild_id: Optional[int] = data.get("guild_id")
        self.channel_id: Optional[SnowFlake] = data.get("channel_id")
        self.app_permissions: Optional[int] = data.get("app_permissions")
        self.locale: Optional[str] = data.get("locale")
        self.guild_locale: Optional[str] = data.get("guild_locale")
        self.user: Union[User, Member]
        self._data: Optional[dict] = None
        self.data: Optional[ApplicationCommandData] = (
            ApplicationCommandData(**self._data) if self._data else None
        )
        if self.guild_id:
            try:
                member = data["member"]
            except:
                pass
            else:
                self.user = Member(**member)
        else:
            self.user = User(**data["user"])
        self.channel: Optional[Any] = data.get("channel")
        self.__message: Optional[dict] = data.get("message")
        self.message: Optional[Message]
        if self.__message is not None:
            self.message = Message(_request=self._request, **self.__message)

    @property
    def bot(self) -> Bot:
        """
        :class:`Bot`: The bot that is handling this interaction.
        """
        return self._request.app

    @property
    def is_done(self) -> bool:
        """
        :class:`bool`: Indicates whether an interaction response has been done before.
        An interaction can only be responded to once.
        """
        return self._is_response_done

    @property
    def is_application_command(self) -> bool:
        """
        The is_application_command function checks if the interaction type is an application command.
        """
        return self.type == InteractionType.APPLICATION_COMMAND.value

    @property
    def is_autocomplete(self) -> bool:
        """
        The is_autocomplete function checks if the interaction type is an autocomplete.
        """
        return self.type == InteractionType.APPLICATION_COMMAND_AUTOCOMPLETE.value

    @property
    def is_modal_submit(self) -> bool:
        """
        The is_modal_submit function checks if the interaction type is a modal submit.
        """
        return self.type == InteractionType.MODAL_SUBMIT.value

    @property
    def is_ping(self) -> bool:
        """
        The is_ping function checks if the interaction type is a ping.
        """
        return self.type == InteractionType.PING.value

    @property
    def is_component(self) -> bool:
        """
        The is_component function checks if the interaction is a component.
        """
        return self.type == InteractionType.MESSAGE_COMPONENT.value

    @property
    def is_responded(self) -> bool:
        """
        The is_responded function checks if the response is done.
        """
        return self._is_response_done

    @property
    def namespace(self) -> Namespace:
        if self.type not in (InteractionType.APPLICATION_COMMAND.value, InteractionType.APPLICATION_COMMAND_AUTOCOMPLETE.value):
            return Namespace(**{})
        if (data := self.data) is None or (options := data.options) is None:
            return Namespace(**{})
        kwargs = {}
        filtered_options: List[ApplicationCommandOption] = list()
        return Namespace(**{})

    async def fetch_guild(self) -> Optional[Guild]:
        """
        This function is a coroutine that returns the Guild object for this interaction.
        It is used to get the guild object from its ID, which is stored in self.guild_id.

        Returns
        -------
        Optional[Guild]:
            A guild object if the guild_id is not none.

        :doc-author: Trelent
        """
        if self.guild_id is None:
            return None
        return await self.bot.fetch_guild(self.guild_id)

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
        if self.is_responded != False:
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


class Namespace:
    """
    Inspired from discord.py
    """

    def __init__(self, **kwargs) -> None:
        for k, v in kwargs.items():
            self.__dict__[k] = v

    def __getattr__(self, value) -> None:
        return None
