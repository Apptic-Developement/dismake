from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Dict,
    List,
    Literal,
    Optional,
    Sequence,
    TypedDict,
    Union,
)


if TYPE_CHECKING:
    from typing_extensions import NotRequired, Required
    from .snowflake import Snowflake


__all__: Sequence[str] = (
    "ApplicationCommandOptionData",
    "ApplicationCommandOptionChoiceData",
    "ApplicationCommandData",
    "GuildApplicationCommandData",
    "ApplicationCommandPermissionsData",
    "GuildApplicationCommandPermissionsData",
)

ChannelType = Literal[0, 1, 2, 3, 4, 5, 10, 11, 12, 13, 14, 15, 16]


class _BaseApplicationCommandOption(TypedDict):
    name: str
    description: str
    name_localizations: NotRequired[Optional[Dict[str, str]]]
    description_localizations: NotRequired[Optional[Dict[str, str]]]


class _SubCommandCommandOption(_BaseApplicationCommandOption):
    type: Literal[1]
    options: List[_ValueApplicationCommandOption]


class _SubCommandGroupCommandOption(_BaseApplicationCommandOption):
    type: Literal[2]
    options: List[_SubCommandCommandOption]


class _BaseValueApplicationCommandOption(_BaseApplicationCommandOption, total=False):
    required: bool


class _StringApplicationCommandOptionChoice(TypedDict):
    name: str
    name_localizations: NotRequired[Optional[Dict[str, str]]]
    value: str


class _StringApplicationCommandOption(_BaseApplicationCommandOption):
    type: Literal[3]
    choices: NotRequired[List[_StringApplicationCommandOptionChoice]]
    min_length: NotRequired[int]
    max_length: NotRequired[int]
    autocomplete: NotRequired[bool]


class _IntegerApplicationCommandOptionChoice(TypedDict):
    name: str
    name_localizations: NotRequired[Optional[Dict[str, str]]]
    value: int


class _IntegerApplicationCommandOption(_BaseApplicationCommandOption, total=False):
    type: Required[Literal[4]]
    min_value: int
    max_value: int
    choices: List[_IntegerApplicationCommandOptionChoice]
    autocomplete: bool


class _BooleanApplicationCommandOption(_BaseValueApplicationCommandOption):
    type: Literal[5]


class _ChannelApplicationCommandOptionChoice(_BaseApplicationCommandOption):
    type: Literal[7]
    channel_types: NotRequired[List[ChannelType]]


class _NonChannelSnowflakeApplicationCommandOptionChoice(
    _BaseValueApplicationCommandOption
):
    type: Literal[6, 8, 9, 11]


_SnowflakeApplicationCommandOptionChoice = Union[
    _ChannelApplicationCommandOptionChoice,
    _NonChannelSnowflakeApplicationCommandOptionChoice,
]


class _NumberApplicationCommandOptionChoice(TypedDict):
    name: str
    name_localizations: NotRequired[Optional[Dict[str, str]]]
    value: float


class _NumberApplicationCommandOption(_BaseValueApplicationCommandOption, total=False):
    type: Required[Literal[10]]
    min_value: float
    max_value: float
    choices: List[_NumberApplicationCommandOptionChoice]
    autocomplete: bool


_ValueApplicationCommandOption = Union[
    _StringApplicationCommandOption,
    _IntegerApplicationCommandOption,
    _BooleanApplicationCommandOption,
    _SnowflakeApplicationCommandOptionChoice,
    _NumberApplicationCommandOption,
]

ApplicationCommandOptionData = Union[
    _SubCommandGroupCommandOption,
    _SubCommandCommandOption,
    _ValueApplicationCommandOption,
]

ApplicationCommandOptionChoiceData = Union[
    _StringApplicationCommandOptionChoice,
    _IntegerApplicationCommandOptionChoice,
    _NumberApplicationCommandOptionChoice,
]


class _BaseApplicationCommand(TypedDict):
    id: Snowflake
    application_id: Snowflake
    name: str
    dm_permission: NotRequired[Optional[bool]]
    default_member_permissions: NotRequired[Optional[str]]
    nsfw: NotRequired[bool]
    version: Snowflake
    name_localizations: NotRequired[Optional[Dict[str, str]]]
    description_localizations: NotRequired[Optional[Dict[str, str]]]


class _ChatInputApplicationCommand(_BaseApplicationCommand, total=False):
    description: Required[str]
    type: Literal[1]
    options: Union[
        List[_ValueApplicationCommandOption],
        List[Union[_SubCommandCommandOption, _SubCommandGroupCommandOption]],
    ]


class _BaseContextMenuApplicationCommand(_BaseApplicationCommand):
    description: Literal[""]


class _UserApplicationCommand(_BaseContextMenuApplicationCommand):
    type: Literal[2]


class _MessageApplicationCommand(_BaseContextMenuApplicationCommand):
    type: Literal[3]


GlobalApplicationCommand = Union[
    _ChatInputApplicationCommand,
    _UserApplicationCommand,
    _MessageApplicationCommand,
]


class _GuildChatInputApplicationCommand(_ChatInputApplicationCommand):
    guild_id: Snowflake


class _GuildUserApplicationCommand(_UserApplicationCommand):
    guild_id: Snowflake


class _GuildMessageApplicationCommand(_MessageApplicationCommand):
    guild_id: Snowflake


GuildApplicationCommandData = Union[
    _GuildChatInputApplicationCommand,
    _GuildUserApplicationCommand,
    _GuildMessageApplicationCommand,
]


ApplicationCommandData = Union[
    GlobalApplicationCommand,
    GuildApplicationCommandData,
]


ApplicationCommandPermissionType = Literal[1, 2, 3]


class ApplicationCommandPermissionsData(TypedDict):
    id: Snowflake
    type: ApplicationCommandPermissionType
    permission: bool


class GuildApplicationCommandPermissionsData(TypedDict):
    id: Snowflake
    application_id: Snowflake
    guild_id: Snowflake
    permissions: List[ApplicationCommandPermissionsData]
