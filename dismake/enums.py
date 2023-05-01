from __future__ import annotations

from enum import Enum, IntEnum

__all__ = (
    "DefaultAvatar",
    "InteractionType",
    "InteractionResponseType",
    "InteractionResponseFlags",
    "CommandType",
    "OptionType",
    "MessageFlags",
    "ChannelType",
    "StrEnum",
    "Locale",
    "ComponentTypes",
    "ButtonStyles",
    "TextInputStyle",
)


class StrEnum(str, Enum):
    def __str__(self) -> str:
        return self.value


class DefaultAvatar(Enum):
    blurple = 0
    grey = 1
    gray = 1
    green = 2
    orange = 3
    red = 4

    def __str__(self) -> str:
        return self.name


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


class InteractionResponseFlags(Enum):
    EPHEMERAL = 1 << 6


class CommandType(Enum):
    SLASH = 1
    USER = 2
    MESSAGE = 3


class OptionType(Enum):
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


class MessageFlags(Enum):
    CROSSPOSTED = 1 << 0
    IS_CROSSPOST = 1 << 1
    SUPPRESS_EMBEDS = 1 << 2
    SOURCE_MESSAGE_DELETED = 1 << 3
    URGENT = 1 << 4
    HAS_THREAD = 1 << 5
    EPHEMERAL = 1 << 6
    LOADING = 1 << 7
    FAILED_TO_MENTION_SOME_ROLES_IN_THREAD = 1 << 8
    SUPPRESS_NOTIFICATIONS = 1 << 12


class ChannelType:
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


class Locale(StrEnum):
    id = "id"  # Indonesian   Bahasa Indonesia
    da = "da"  # Danish	Dansk
    de = "de"  # 	German	Deutsch
    en_GB = "en-GB"  # 	English, UK	English, UK
    en_US = "en-US"  # 	English, US	English, US
    es_ES = "es-ES"  # 	Spanish	Español
    fr = "fr"  # 	French	Français
    hr = "hr"  # 	Croatian	Hrvatski
    it = "it"  # 	Italian	Italiano
    lt = "lt"  # 	Lithuanian	Lietuviškai
    hu = "hu"  # 	Hungarian	Magyar
    nl = "nl"  # 	Dutch	Nederlands
    no = "no"  # 	Norwegian	Norsk
    pl = "pl"  # 	Polish	Polski
    pt_BR = "pt-BR"  # 	Portuguese, Brazilian	Português do Brasil
    ro = "ro"  # 	Romanian, Romania	Română
    fi = "fi"  # 	Finnish	Suomi
    sv_SE = "sv-SE"  # 	Swedish	Svenska
    vi = "vi"  # 	Vietnamese	Tiếng Việt
    tr = "tr"  # 	Turkish	Türkçe
    cs = "cs"  # 	Czech	Čeština
    el = "el"  # 	Greek	Ελληνικά
    bg = "bg"  # 	Bulgarian	български
    ru = "ru"  # 	Russian	Pусский
    uk = "uk"  # 	Ukrainian	Українська
    hi = "hi"  # 	Hindi	हिन्दी
    th = "th"  # 	Thai	ไทย
    zh_CN = "zh-CN"  # 	Chinese, China	中文
    ja = "ja"  # 	Japanese	日本語
    zh_TW = "zh-TW"  # 	Chinese, Taiwan	繁體中文
    ko = "ko"  # 	Korean	한국어


class ComponentTypes(IntEnum):
    ACTION_ROW = 1
    BUTTON = 2
    SELECT_MENU = 3
    TEXT_INPUT = 4


class ButtonStyles(IntEnum):
    PRIMARY = primary = 1
    SECONDARY = secondary = 2
    SUCCESS = success = 3
    DANGER = danger = 4
    LINK = link = 5


class TextInputStyle(IntEnum):
    SHORT = short = 1
    PARAGRAPH = paragraph = 2
