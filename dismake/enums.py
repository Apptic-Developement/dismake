from __future__ import annotations

from typing import Sequence
from enum import Enum

__all__: Sequence[str] = (
    "InteractionType",
    "InteractionResponseType",
    "ApplicationCommandOptionType",
    "ChannelType",
    "DefaultAvatar",
    "Locale",
    "ApplicationCommandType"
)


class InteractionType(Enum):
    PING = 1
    APPLICATION_COMMAND = 2
    MESSAGE_COMPONENT = 3
    APPLICATION_COMMAND_AUTOCOMPLETE = 4
    MODAL_SUBMIT = 5


class InteractionResponseType(Enum):
    PONG = 1
    CHANNEL_MESSAGE_WITH_SOURCE = 4
    DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE = 5
    DEFERRED_UPDATE_MESSAGE = 6
    UPDATE_MESSAGE = 7
    APPLICATION_COMMAND_AUTOCOMPLETE_RESULT = 8
    MODAL = 9


class ApplicationCommandOptionType(Enum):
    SUB_COMMAND = 1
    SUB_COMMAND_GROUP = 2
    STRING = 3
    INTEGER = 4
    BOOLEAN = 5
    USER = 6
    CHANNEL = 7
    ROLE = 8
    MENTIONABLE = 9
    NUMBER = 10
    ATTACHMENT = 11


class ChannelType(Enum):
    GUILD_TEXT = 0
    DM = 1
    GUILD_VOICE = 2
    GROUP_DM = 3
    GUILD_CATEGORY = 4
    GUILD_ANNOUNCEMENT = 5
    ANNOUNCEMENT_THREAD = 10
    PUBLIC_THREAD = 11
    PRIVATE_THREAD = 12
    GUILD_STAGE_VOICE = 13
    GUILD_DIRECTORY = 14
    GUILD_FORUM = 15
    GUILD_MEDIA = 16


class DefaultAvatar(Enum):
    blurple = 0
    grey = 1
    gray = 1
    green = 2
    orange = 3
    red = 4
    pink = 5

    def __str__(self) -> str:
        return self.name


class Locale(str, Enum):
    ID = "id"
    DA = "da"
    DE = "de"
    EN_GB = "en-GB"
    EN_US = "en-US"
    ES_ES = "es-ES"
    FR = "fr"
    HR = "hr"
    IT = "it"
    LT = "lt"
    HU = "hu"
    NL = "nl"
    NO = "no"
    PL = "pl"
    PT_BR = "pt-BR"
    RO = "ro"
    FI = "fi"
    SV_SE = "sv-SE"
    VI = "vi"
    TR = "tr"
    CS = "cs"
    EL = "el"
    BG = "bg"
    RU = "ru"
    UK = "uk"
    HI = "hi"
    TH = "th"
    ZH_CN = "zh-CN"
    JA = "ja"
    ZH_TW = "zh-TW"
    KO = "ko"

class ApplicationCommandType(Enum):
    CHAT_INPUT = 1
    USER = 2
    MESSAGE = 3