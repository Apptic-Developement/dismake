from __future__ import annotations

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from typing_extensions import Self

    from dismake import Client
    from dismake.types import Guild as GuildPayload


__all__ = ("Guild",)


class Guild:
    def __init__(self, client: Client, payload: GuildPayload):
        self._client = client
        self._payload = payload
        self.id: int = int(payload["id"])
        self.name: str = payload["name"]
        self._icon: Optional[str] = payload.get("icon")
        # self.icon_hash: NotRequired[str]
        # self.splash: NotRequired[str]
        # self.discovery_splash: NotRequired[str]
        # self.owner: NotRequired[bool]
        # self.owner_id: Snowflake
        # self.permissions: NotRequired[str]
        # self.afk_channel_id: NotRequired[Snowflake]
        # self.afk_timeout: int
        # self.widget_enabled: NotRequired[bool]
        # self.widget_channel_id: NotRequired[Snowflake]
        # self.verification_level: VerificationLevel
        # self.default_message_notifications: DefaultMessageNotifications
        # self.explicit_content_filter: ExplicitContentFilterLevel
        # self.roles: list[Role]
        # self.emojis: Any
        # self.features: list[GuildFeatures]
        # self.mfa_level: MFALevel
        # self.application_id: NotRequired[Snowflake]
        # self.system_channel_id: NotRequired[Snowflake]
        # self.system_channel_flags: int
        # self.rules_channel_id: NotRequired[Snowflake]
        # self.max_presences: NotRequired[int]
        # self.max_members: NotRequired[int]
        # self.vanity_url_code: NotRequired[str]
        # self.description: NotRequired[str]
        # self.banner: NotRequired[str]
        # self.premium_tier: PremiumTier
        # self.premium_subscription_count: NotRequired[int]
        # self.preferred_locale: str
        # self.public_updates_channel_id: NotRequired[Snowflake]
        # self.max_video_channel_users: NotRequired[int]
        # self.max_stage_video_channel_users: NotRequired[int]
        # self.approximate_member_count: NotRequired[int]
        # self.approximate_presence_count: NotRequired[int]
        # self.welcome_screen: NotRequired[WelcomeScreen]
        # self.nsfw_level: NSFWLevel
        # self.stickers: Any
        # self.premium_progress_bar_enabled: bool
        # self.safety_alerts_channel_id: NotRequired[Snowflake]

    def __eq__(self, obj: Self) -> bool:
        return self.id == obj.id
