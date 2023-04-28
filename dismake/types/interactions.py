from __future__ import annotations

from typing import Any, Dict, List, TypedDict, TYPE_CHECKING, Union

from .snowflake import SnowFlake

if TYPE_CHECKING:
    from typing_extensions import NotRequired
    from .user import User, Member
    from .role import Role


__all__ = (
    "Interaction",
    "ApplicationCommandData",
    "ApplicationCommandOptions",
    "MessageComponentData",
    "ModalSubmitData",
    "InteractionData",
)


class Interaction(TypedDict):
    id: SnowFlake
    token: str
    application_id: SnowFlake
    version: int
    type: int
    data: NotRequired[InteractionData]
    guild_id: NotRequired[SnowFlake]
    channel: NotRequired[Any]  # TODO
    channel_id: NotRequired[SnowFlake]
    member: NotRequired[Any]  # TODO
    user: NotRequired[Any]  # TODO
    message: NotRequired[Any]  # TODO
    app_permissions: NotRequired[str]
    locale: NotRequired[str]
    guild_locale: NotRequired[str]


class ApplicationCommandData(TypedDict):
    id: SnowFlake
    name: str
    type: int
    resolved: NotRequired[ResolvedData]
    options: NotRequired[List[ApplicationCommandOptions]]
    guild_id: NotRequired[SnowFlake]
    target_id: NotRequired[SnowFlake]


class MessageComponentData(TypedDict):
    custom_id: str
    component_type: int
    values: NotRequired[List[Any]]  # TODO


class ModalSubmitData(TypedDict):
    custom_id: str
    components: List[Any]  # TODO


class ResolvedData(TypedDict):
    users: NotRequired[Dict[str, User]]
    members: NotRequired[Dict[str, Member]]
    roles: NotRequired[Dict[str, Role]]
    channels: NotRequired[Any]  # TODO
    messages: NotRequired[Any]  # TODO
    attachments: NotRequired[Any]  # TODO


class ApplicationCommandOptions(TypedDict):
    name: str
    type: int
    value: NotRequired[Union[int, str, bool, float]]
    options: NotRequired[List[ApplicationCommandOptions]]
    focused: NotRequired[bool]


InteractionData = Union[ApplicationCommandData, MessageComponentData, ModalSubmitData]
