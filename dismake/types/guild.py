from __future__ import annotations
from typing import TYPE_CHECKING, Literal, TypedDict, Any

if TYPE_CHECKING:
    from .snowflake import Snowflake
    from .role import Role
    from typing_extensions import NotRequired


__all__ = ("Guild",)

PremiumTier = Literal[0, 1, 2, 3]
VerificationLevel = Literal[0, 1, 2, 3, 4]
NSFWLevel = Literal[0, 1, 2, 3]
DefaultMessageNotifications = Literal[0, 1]
ExplicitContentFilterLevel = Literal[0, 1, 2]
MFALevel = Literal[0, 1]
GuildFeatures = Literal[
    "ANIMATED_BANNER",
    "ANIMATED_ICON",
    "APPLICATION_COMMAND_PERMISSIONS_V2",
    "AUTO_MODERATION",
    "BANNER",
    "COMMUNITY",
    "CREATOR_MONETIZABLE_PROVISIONAL",
    "CREATOR_STORE_PAGE",
    "DEVELOPER_SUPPORT_SERVER",
    "DISCOVERABLE",
    "FEATURABLE",
    "INVITES_DISABLED",
    "INVITE_SPLASH",
    "MEMBER_VERIFICATION_GATE_ENABLED",
    "MORE_STICKERS",
    "NEWS",
    "PARTNERED",
    "PREVIEW_ENABLED",
    "RAID_ALERTS_DISABLED",
    "ROLE_ICONS",
    "ROLE_SUBSCRIPTIONS_AVAILABLE_FOR_PURCHASE",
    "ROLE_SUBSCRIPTIONS_ENABLED",
    "TICKETED_EVENTS_ENABLED",
    "VANITY_URL",
    "VERIFIED",
    "VIP_REGIONS",
    "WELCOME_SCREEN_ENABLED",
]


class WelcomeScreenChannel(TypedDict):
    channel_id: Snowflake
    description: str
    emoji_id: NotRequired[Snowflake]
    emoji_name: NotRequired[str]


class WelcomeScreen(TypedDict):
    description: NotRequired[str]
    welcome_channels: list[WelcomeScreenChannel]


class Guild(TypedDict):
    id: Snowflake
    name: str
    icon: NotRequired[str]
    icon_hash: NotRequired[str]
    splash: NotRequired[str]
    discovery_splash: NotRequired[str]
    owner: NotRequired[bool]
    owner_id: Snowflake
    permissions: NotRequired[str]
    afk_channel_id: NotRequired[Snowflake]
    afk_timeout: int
    widget_enabled: NotRequired[bool]
    widget_channel_id: NotRequired[Snowflake]
    verification_level: VerificationLevel
    default_message_notifications: DefaultMessageNotifications
    explicit_content_filter: ExplicitContentFilterLevel
    roles: list[Role]
    emojis: Any
    features: list[GuildFeatures]
    mfa_level: MFALevel
    application_id: NotRequired[Snowflake]
    system_channel_id: NotRequired[Snowflake]
    system_channel_flags: int
    rules_channel_id: NotRequired[Snowflake]
    max_presences: NotRequired[int]
    max_members: NotRequired[int]
    vanity_url_code: NotRequired[str]
    description: NotRequired[str]
    banner: NotRequired[str]
    premium_tier: PremiumTier
    premium_subscription_count: NotRequired[int]
    preferred_locale: str
    public_updates_channel_id: NotRequired[Snowflake]
    max_video_channel_users: NotRequired[int]
    max_stage_video_channel_users: NotRequired[int]
    approximate_member_count: NotRequired[int]
    approximate_presence_count: NotRequired[int]
    welcome_screen: NotRequired[WelcomeScreen]
    nsfw_level: NSFWLevel
    stickers: Any
    premium_progress_bar_enabled: bool
    safety_alerts_channel_id: NotRequired[Snowflake]
