from __future__ import annotations

from typing import Optional, List, Any, Dict
from datetime import datetime
from pydantic import BaseModel, validator
from .user import Member, User
from ..types import SnowFlake
from enum import Enum
from ..asset import Asset


class Ban(BaseModel):
    reason: str
    user: User


class GuildWidget(BaseModel):
    enabled: bool
    channel_id: SnowFlake


class GuildWidgetImageStyle(Enum):
    shield = "shield"
    banner1 = "banner1"
    banner2 = "banner2"
    banner3 = "banner3"
    banner4 = "banner4"


class WelcomeChannel(BaseModel):
    channel_id: SnowFlake
    description: str
    emoji_id: Optional[SnowFlake]
    emoji_name: str


class WelcomeScreen(BaseModel):
    description: str
    welcome_channels: List[WelcomeChannel]


class Guild(BaseModel):
    id: SnowFlake
    name: str
    icon: Optional[str]
    afk_channel_id: Optional[SnowFlake]
    afk_timeout: Optional[int]
    application_command_count: Optional[int]
    application_command_counts: Optional[Dict[str, int]]
    application_id: Optional[SnowFlake]
    banner: Optional[str]
    # channels: Dict[SnowFlake, Channel] = dict() TODO: Channel
    # default_message_notifications: GuildMessageNotification TODO
    description: Optional[str]
    discovery_splash: Optional[str]
    embedded_activities: List[Any] = []
    # emojis: Dict[SnowFlake, Emoji] TODO: Emoji
    # explicit_content_filter: ExplicitContentFilterLevel TODO
    features: List[str]
    guild_hashes: Dict[Any, Any] = {}
    # guild_scheduled_events: Dict[SnowFlake, GuildScheduledEvent] = {} TODO GuildSheduledEvent
    hub_type: Optional[bool]
    joined_at: Optional[datetime]
    large: bool = False
    lazy: Optional[bool]
    max_members: int
    max_video_channel_users: Optional[int]
    member_count: int = 0
    members: Dict[SnowFlake, Member] = {}
    # mfa_level: MFALevel TODO
    nsfw: bool
    # nsfw_level: NSFWLevel TODO
    owner_id: SnowFlake
    preferred_locale: str
    premium_progress_bar_enabled: Optional[bool]
    premium_subscription_count: int
    # premium_tier: PremiumTierLevel TODO
    presences: Optional[List[Dict[str, Any]]]
    public_updates_channel_id: Optional[SnowFlake]
    # roles: Dict[SnowFlake, Role] TODO: Role
    rules_channel_id: Optional[SnowFlake]
    splash: Optional[str]
    stage_instances: Optional[List[Any]] = list()
    # stickers: Optional[Dict[SnowFlake, Sticker]] = dict() TODO Sticker
    system_channel_flags: Optional[int]
    system_channel_id: Optional[SnowFlake]
    # threads: Optional[Dict[SnowFlake, Thread]] = dict() TODO: Thread
    unavailable: Optional[bool]
    vanity_url_code: Optional[str]
    # verification_level: VerificationLevel TODO
    voice_states: Optional[List[Any]] = list()
    created_at: Optional[datetime]

    @property
    def display_banner(self) -> Optional[Asset]:
        if self.banner:
            return Asset.from_guild_banner(self.banner, int(self.id))

    @property
    def display_icon(self) -> Optional[Asset]:
        if self.icon:
            return Asset.from_guild_icon(self.icon, int(self.id))
