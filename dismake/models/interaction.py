from __future__ import annotations
from re import I

from typing import Any, List, Optional, TYPE_CHECKING, Union, Dict, TYPE_CHECKING
from pydantic import BaseModel
from .components import SelectOption
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
    "MessageComponentData"
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

class MessageComponentData(BaseModel):
    custom_id: str
    component_type: int
    values: Optional[List[SelectOption]]


class ModalSubmitData(BaseModel):
    custom_id: str
    # components	array of message components	the values submitted by the user

import discord.interactions
class Interaction:
    """Represents a Discord interaction.

    An interaction happens when a user does an action that needs to
    be notified. Current examples are slash commands and components.

    Parameters
    -----------
    request: Request
        The request object.
    data: Dict[str, Any]
        The interaction data
    """
    __slots__ = (
        "_request",
        "_is_response_done",
        "id",
        "application_id",
        "type",
        "token",
        "version",
        "guild_id",
        "channel_id",
        "app_permissions",
        "locale",
        "guild_locale",
        "user",
        "_data",
        "data",
        "channel",
        "__message",
        "message",
    )
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
        self._data: Optional[dict] = data.get("data")
        self.data: Optional[
            Union[ApplicationCommandData, ModalSubmitData, MessageComponentData]
        ]
        if self.is_application_command or self.is_autocomplete:
            self.data = ApplicationCommandData(**self._data) if self._data else None
        elif self.is_message_component:
            self.data = MessageComponentData(**self._data) if self._data else None
        else:
            self.data = ModalSubmitData(**self._data) if self._data else None
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
    def is_message_component(self) -> bool:
        """
        The is_component function checks if the interaction is a component.
        """
        return self.type == InteractionType.MESSAGE_COMPONENT.value

    @property
    def is_responded(self) -> bool:
        """
        :class:`bool`: Indicates whether an interaction response has been done before.
        An interaction can only be responded to once.
        """
        return self._is_response_done

    @property
    def namespace(self) -> Namespace:
        if not isinstance(self.data, ApplicationCommandData):
            return Namespace(**{})
        if (data := self.data) is None or (options := data.options) is None:
            return Namespace(**{})
        kwargs = {}
        filtered_options: List[ApplicationCommandOption] = list()
        for option in options:
            if option.type == OptionType.SUB_COMMAND.value and option.options:
                for sub_command_option in option.options:
                    filtered_options.append(sub_command_option)
            elif option.type == OptionType.SUB_COMMAND_GROUP.value and option.options:
                for sub_command_groups in option.options:
                    if sub_command_groups.options:
                        for sub_command in sub_command_groups.options:
                            if sub_command.options:
                                for sub_command_option in sub_command.options:
                                    filtered_options.append(sub_command_option)
            else:
                filtered_options.append(option)

        if not filtered_options:
            return Namespace(**{})

        for foption in filtered_options:
            if foption.type == OptionType.USER.value:
                if data.resolved is not None and data.resolved.users is not None:
                    kwargs[foption.name.replace("-", "_")] = data.resolved.users.get(str(foption.value))
                else:
                    continue
            elif foption.type == OptionType.ROLE.value:
                if data.resolved is not None and data.resolved.roles is not None:
                    kwargs[foption.name.replace("-", "_")] = data.resolved.roles.get(str(foption.value))
                else:
                    continue
            else:
                kwargs[foption.name.replace("-", "_")] = foption.value
        return Namespace(**kwargs)

    async def fetch_guild(self) -> Optional[Guild]:
        """
        This function is a coroutine that returns the Guild object for this interaction.
        It is used to get the guild object from its ID, which is stored in self.guild_id.

        Returns
        -------
        Optional[Guild]:
            A guild object if the guild_id is not none.
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
        self._is_response_done = True

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
        self._is_response_done = True

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

    async def edit_message(
        self, content: str, *, tts: bool = False, house: Optional[House] = None
    ):
        if not self.is_message_component:
            return
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
class Namespace:
    """
    Inspired from discord.py
    """

    def __init__(self, **kwargs) -> None:
        for k, v in kwargs.items():
            self.__dict__[k] = v

    def __getattr__(self, value) -> None:
        return None
