from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    List,
    Literal,
    Sequence,
    TypedDict,
    Union,
)


if TYPE_CHECKING:
    from typing_extensions import NotRequired
    from .snowflake import Snowflake
    from .user import UserData
    from .member import MemberData
    from .message import MessageData
    from .role import RoleData


__all__: Sequence[str] = ("InteractionData",)

InteractionType = Literal[1, 2, 3, 4, 5]
class MessageInteraction(TypedDict):
    id: Snowflake
    type: InteractionData
    name: str
    user: UserData
    member: NotRequired[MemberData]


class ResolvedData(TypedDict, total=False):
    users: Dict[str, UserData]
    members: Dict[str, MemberData]
    roles: Dict[str, RoleData]
    channels: Dict[str, Any]
    messages: Dict[str, MessageData]
    attachments: Dict[str, Any]


class _BaseApplicationCommandInteractionDataOption(TypedDict):
    name: str


class _CommandGroupApplicationCommandInteractionDataOption(
    _BaseApplicationCommandInteractionDataOption
):
    type: Literal[1, 2]
    options: List[ApplicationCommandInteractionDataOption]


class _BaseValueApplicationCommandInteractionDataOption(
    _BaseApplicationCommandInteractionDataOption, total=False
):
    focused: bool


class _StringValueApplicationCommandInteractionDataOption(
    _BaseValueApplicationCommandInteractionDataOption
):
    type: Literal[3]
    value: str


class _IntegerValueApplicationCommandInteractionDataOption(
    _BaseValueApplicationCommandInteractionDataOption
):
    type: Literal[4]
    value: int


class _BooleanValueApplicationCommandInteractionDataOption(
    _BaseValueApplicationCommandInteractionDataOption
):
    type: Literal[5]
    value: bool


class _SnowflakeValueApplicationCommandInteractionDataOption(
    _BaseValueApplicationCommandInteractionDataOption
):
    type: Literal[6, 7, 8, 9, 11]
    value: Snowflake


class _NumberValueApplicationCommandInteractionDataOption(
    _BaseValueApplicationCommandInteractionDataOption
):
    type: Literal[10]
    value: float


_ValueApplicationCommandInteractionDataOption = Union[
    _StringValueApplicationCommandInteractionDataOption,
    _IntegerValueApplicationCommandInteractionDataOption,
    _BooleanValueApplicationCommandInteractionDataOption,
    _SnowflakeValueApplicationCommandInteractionDataOption,
    _NumberValueApplicationCommandInteractionDataOption,
]
ApplicationCommandInteractionDataOption = Union[
    _CommandGroupApplicationCommandInteractionDataOption,
    _ValueApplicationCommandInteractionDataOption,
]


class ApplicationCommandInteractionData(TypedDict):
    id: Snowflake
    name: str
    type: int
    resolved: NotRequired[ResolvedData]
    options: NotRequired[ApplicationCommandInteractionDataOption]
    guild_id: NotRequired[Snowflake]
    target_id: NotRequired[Snowflake]


class _BaseMessageComponentInteractionData(TypedDict):
    custom_id: str


class ButtonMessageComponentInteractionData(_BaseMessageComponentInteractionData):
    component_type: Literal[2]


class SelectMessageComponentInteractionData(_BaseMessageComponentInteractionData):
    component_type: Literal[3, 5, 6, 7, 8]
    values: List[str]
    resolved: NotRequired[ResolvedData]


MessageComponentInteractionData = Union[
    ButtonMessageComponentInteractionData, SelectMessageComponentInteractionData
]


class ModalSubmitTextInputInteractionData(TypedDict):
    type: Literal[4]
    custom_id: str
    value: str


ModalSubmitComponentItemInteractionData = ModalSubmitTextInputInteractionData


class ModalSubmitActionRowInteractionData(TypedDict):
    type: Literal[1]
    components: List[ModalSubmitComponentItemInteractionData]


ModalSubmitComponentInteractionData = Union[
    ModalSubmitActionRowInteractionData, ModalSubmitComponentItemInteractionData
]


class ModalSubmitInteractionData(TypedDict):
    custom_id: str
    components: List[ModalSubmitComponentInteractionData]


class _BaseInteraction(TypedDict):
    id: Snowflake
    application_id: Snowflake
    guild_id: NotRequired[Snowflake]
    channel: NotRequired[Any]
    channel_id: NotRequired[Snowflake]
    member: NotRequired[MemberData]
    user: NotRequired[UserData]
    token: str
    version: Literal[1]
    message: NotRequired[MessageData]
    app_permissions: NotRequired[str]
    locale: NotRequired[str]
    guild_locale: NotRequired[str]


class PingInteraction(_BaseInteraction):
    type: Literal[1]


class ApplicationCommandInteraction(_BaseInteraction):
    type: Literal[2, 4]
    data: ApplicationCommandInteractionData


class MessageComponentInteraction(_BaseInteraction):
    type: Literal[3]
    data: MessageComponentInteractionData


class ModalSubmitInteraction(_BaseInteraction):
    type: Literal[5]
    data: ModalSubmitInteractionData


InteractionData = Union[
    PingInteraction,
    ApplicationCommandInteraction,
    MessageComponentInteraction,
    ModalSubmitInteraction,
]
