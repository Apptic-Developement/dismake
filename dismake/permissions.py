from __future__ import annotations

from typing import TYPE_CHECKING
from enum import Flag

# from .flags import BaseFlags, alias_flag_value, fill_with_flags, flag_value

if TYPE_CHECKING:
    from typing_extensions import Self
__all__ = ("Permissions",)


class Permissions(Flag):
    NONE = 0
    """Empty permission."""

    CREATE_INSTANT_INVITE = 1 << 0
    """Allows creation of instant invites."""

    KICK_MEMBERS = 1 << 1
    """Allows kicking members.

    .. note::
        In guilds with server-wide 2FA enabled this permission can only be used
        by users who have two-factor authentication enabled on their account
        (or their owner's account in the case of bot users) and the guild owner.
    """

    BAN_MEMBERS = 1 << 2
    """Allows banning members.

    .. note::
        In guilds with server-wide 2FA enabled this permission can only be used
        by users who have two-factor authentication enabled on their account
        (or their owner's account in the case of bot users) and the guild owner.
    """

    ADMINISTRATOR = 1 << 3
    """Allows all permissions and bypasses channel permission overwrites.

    .. note::
        In guilds with server-wide 2FA enabled this permission can only be used
        by users who have two-factor authentication enabled on their account
        (or their owner's account in the case of bot users) and the guild owner.
    """

    MANAGE_CHANNELS = 1 << 4
    """Allows management and editing of channels.

    .. note::
        In guilds with server-wide 2FA enabled this permission can only be used
        by users who have two-factor authentication enabled on their account
        (or their owner's account in the case of bot users) and the guild owner.
    """

    MANAGE_GUILD = 1 << 5
    """Allows management and editing of the guild.

    .. note::
        In guilds with server-wide 2FA enabled this permission can only be used
        by users who have two-factor authentication enabled on their account
        (or their owner's account in the case of bot users) and the guild owner.
    """

    ADD_REACTIONS = 1 << 6
    """Allows for the addition of reactions to messages."""

    VIEW_AUDIT_LOG = 1 << 7
    """Allows for viewing of audit logs."""

    PRIORITY_SPEAKER = 1 << 8
    """Allows for using priority speaker in a voice channel."""

    STREAM = 1 << 9
    """Allows the user to go live."""

    VIEW_CHANNEL = 1 << 10
    """Allows guild members to view a channel, which includes reading messages in text channels."""

    SEND_MESSAGES = 1 << 11
    """Allows for sending messages in a channel."""

    SEND_TTS_MESSAGES = 1 << 12
    """Allows for sending of `/tts` messages."""

    MANAGE_MESSAGES = 1 << 13
    """Allows for deletion of other users messages.

    .. note::
        In guilds with server-wide 2FA enabled this permission can only be used
        by users who have two-factor authentication enabled on their account
        (or their owner's account in the case of bot users) and the guild owner.
    """

    EMBED_LINKS = 1 << 14
    """Links sent by users with this permission will be auto-embedded."""

    ATTACH_FILES = 1 << 15
    """Allows for uploading images and files."""

    READ_MESSAGE_HISTORY = 1 << 16
    """Allows for reading of message history."""

    MENTION_ROLES = 1 << 17
    """Allows for using the `@everyone`, `@here` and `@role` (regardless of its mention status) tag to notify users."""

    USE_EXTERNAL_EMOJIS = 1 << 18
    """Allows the usage of custom emojis from other guilds."""

    VIEW_GUILD_INSIGHTS = 1 << 19
    """Allows the user to view guild insights for eligible guilds."""

    CONNECT = 1 << 20
    """Allows for joining of a voice channel."""

    SPEAK = 1 << 21
    """Allows for speaking in a voice channel."""

    MUTE_MEMBERS = 1 << 22
    """Allows for muting members in a voice channel."""

    DEAFEN_MEMBERS = 1 << 23
    """Allows for deafening of members in a voice channel."""

    MOVE_MEMBERS = 1 << 24
    """Allows for moving of members between voice channels."""

    USE_VOICE_ACTIVITY = 1 << 25
    """Allows for using voice-activity-detection in a voice channel."""

    CHANGE_NICKNAME = 1 << 26
    """Allows for modification of own nickname."""

    MANAGE_NICKNAMES = 1 << 27
    """Allows for modification of other users nicknames."""

    MANAGE_ROLES = 1 << 28
    """Allows management and editing of roles.

    .. note::
        In guilds with server-wide 2FA enabled this permission can only be used
        by users who have two-factor authentication enabled on their account
        (or their owner's account in the case of bot users) and the guild owner.
    """

    MANAGE_WEBHOOKS = 1 << 29
    """Allows management and editing of webhooks.

    .. note::
        In guilds with server-wide 2FA enabled this permission can only be used
        by users who have two-factor authentication enabled on their account
        (or their owner's account in the case of bot users) and the guild owner.
    """

    MANAGE_EMOJIS_AND_STICKERS = 1 << 30
    """Allows management and editing of emojis and stickers.

    .. note::
        In guilds with server-wide 2FA enabled this permission can only be used
        by users who have two-factor authentication enabled on their account
        (or their owner's account in the case of bot users) and the guild owner.
    """

    USE_APPLICATION_COMMANDS = 1 << 31
    """Allows for using the application commands of guild integrations within a text channel."""

    REQUEST_TO_SPEAK = 1 << 32
    """Allows for requesting to speak in stage channels.

    .. warning::
        This permissions is currently defined as being "under active
        development" by Discord meaning that "it may be changed or removed"
        without warning.
    """

    MANAGE_EVENTS = 1 << 33
    """Allows for creating, editing, and deleting scheduled events	"""

    MANAGE_THREADS = 1 << 34
    """Allows for deleting and archiving threads, and viewing all private threads.

     .. note::
        In guilds with server-wide 2FA enabled this permission can only be used
        by users who have two-factor authentication enabled on their account
        (or their owner's account in the case of bot users) and the guild owner.
    """

    CREATE_PUBLIC_THREADS = 1 << 35
    """Allows for creating threads."""

    CREATE_PRIVATE_THREADS = 1 << 36
    """Allows for creating private threads."""

    USE_EXTERNAL_STICKERS = 1 << 37
    """Allows the usage of custom stickers from other servers."""

    SEND_MESSAGES_IN_THREADS = 1 << 38
    """Allows for sending messages in threads."""

    START_EMBEDDED_ACTIVITIES = 1 << 39
    """Allows for launching activities (applications with the `EMBEDDED` flag) in a voice channel."""

    MODERATE_MEMBERS = 1 << 40
    """Allows for timing out members."""

    @classmethod
    def all_permissions(cls) -> Permissions:
        """Get an instance of `Permissions` with all the known permissions.

        Returns
        -------
        Permissions
            A permissions instance with all the known permissions.
        """
        all_perms = Permissions.NONE
        for perm in Permissions:
            all_perms |= perm

        return all_perms


# class permission_alias(alias_flag_value):
#     alias: str


# def make_permission_alias(
#     alias: str,
# ) -> Callable[[Callable[[Any], int]], permission_alias]:
#     def decorator(func: Callable[[Any], int]) -> permission_alias:
#         ret = permission_alias(func)
#         ret.alias = alias
#         return ret

#     return decorator


# @fill_with_flags()
# class Permissions(BaseFlags):
#     def __init__(self, permissions: int = 0, **kwargs: bool) -> None:
#         if not isinstance(permissions, int):
#             raise TypeError(
#                 f"Expected int parameter, received {permissions.__class__.__name__} instead."
#             )
#         self.value = permissions
#         for key, value in kwargs.items():
#             if key not in self.VALID_FLAGS:
#                 raise TypeError(f"{key!r} is not a valid permission name.")
#             setattr(self, key, value)

#     def is_subset(self, other: Permissions) -> bool:
#         """Returns ``True`` if self has the same or fewer permissions as other."""
#         if isinstance(other, Permissions):
#             return (self.value & other.value) == self.value
#         else:
#             raise TypeError(
#                 f"cannot compare {self.__class__.__name__} with {other.__class__.__name__}"
#             )

#     def is_superset(self, other: Permissions) -> bool:
#         """Returns ``True`` if self has the same or more permissions as other."""
#         if isinstance(other, Permissions):
#             return (self.value | other.value) == self.value
#         else:
#             raise TypeError(
#                 f"cannot compare {self.__class__.__name__} with {other.__class__.__name__}"
#             )

#     def is_strict_subset(self, other: Permissions) -> bool:
#         """Returns ``True`` if the permissions on other are a strict subset of those on self."""
#         return self.is_subset(other) and self != other

#     def is_strict_superset(self, other: Permissions) -> bool:
#         """Returns ``True`` if the permissions on other are a strict superset of those on self."""
#         return self.is_superset(other) and self != other

#     __le__ = is_subset
#     __ge__ = is_superset
#     __lt__ = is_strict_subset
#     __gt__ = is_strict_superset

#     @classmethod
#     def none(cls) -> Self:
#         """A factory method that creates a :class:`Permissions` with all
#         permissions set to ``False``."""
#         return cls(0)

#     @classmethod
#     def all(cls) -> Self:
#         """A factory method that creates a :class:`Permissions` with all
#         permissions set to ``True``.
#         """
#         return cls(0b11111111111111111111111111111111111111111)

#     @classmethod
#     def _timeout_mask(cls) -> int:
#         p = cls.all()
#         p.view_channel = False
#         p.read_message_history = False
#         return ~p.value

#     @classmethod
#     def _dm_permissions(cls) -> Self:
#         base = cls.text()
#         base.read_messages = True
#         base.send_tts_messages = False
#         base.manage_messages = False
#         base.create_private_threads = False
#         base.create_public_threads = False
#         base.manage_threads = False
#         base.send_messages_in_threads = False
#         return base

#     @classmethod
#     def all_channel(cls) -> Self:
#         """A :class:`Permissions` with all channel-specific permissions set to
#         ``True`` and the guild-specific ones set to ``False``. The guild-specific
#         permissions are currently:

#         - :attr:`manage_emojis`
#         - :attr:`view_audit_log`
#         - :attr:`view_guild_insights`
#         - :attr:`manage_guild`
#         - :attr:`change_nickname`
#         - :attr:`manage_nicknames`
#         - :attr:`kick_members`
#         - :attr:`ban_members`
#         - :attr:`administrator`

#         .. versionchanged:: 1.7
#            Added :attr:`stream`, :attr:`priority_speaker` and :attr:`use_application_commands` permissions.

#         .. versionchanged:: 2.0
#            Added :attr:`create_public_threads`, :attr:`create_private_threads`, :attr:`manage_threads`,
#            :attr:`use_external_stickers`, :attr:`send_messages_in_threads` and
#            :attr:`request_to_speak` permissions.
#         """
#         return cls(0b111110110110011111101111111111101010001)

#     @classmethod
#     def general(cls) -> Self:
#         """A factory method that creates a :class:`Permissions` with all
#         "General" permissions from the official Discord UI set to ``True``.

#         .. versionchanged:: 1.7
#            Permission :attr:`read_messages` is now included in the general permissions, but
#            permissions :attr:`administrator`, :attr:`create_instant_invite`, :attr:`kick_members`,
#            :attr:`ban_members`, :attr:`change_nickname` and :attr:`manage_nicknames` are
#            no longer part of the general permissions.
#         """
#         return cls(0b01110000000010000000010010110000)

#     @classmethod
#     def membership(cls) -> Self:
#         """A factory method that creates a :class:`Permissions` with all
#         "Membership" permissions from the official Discord UI set to ``True``.

#         .. versionadded:: 1.7
#         """
#         return cls(0b10000000000001100000000000000000000000111)

#     @classmethod
#     def text(cls) -> Self:
#         """A factory method that creates a :class:`Permissions` with all
#         "Text" permissions from the official Discord UI set to ``True``.

#         .. versionchanged:: 1.7
#            Permission :attr:`read_messages` is no longer part of the text permissions.
#            Added :attr:`use_application_commands` permission.

#         .. versionchanged:: 2.0
#            Added :attr:`create_public_threads`, :attr:`create_private_threads`, :attr:`manage_threads`,
#            :attr:`send_messages_in_threads` and :attr:`use_external_stickers` permissions.
#         """
#         return cls(0b111110010000000000001111111100001000000)

#     @classmethod
#     def voice(cls) -> Self:
#         """A factory method that creates a :class:`Permissions` with all
#         "Voice" permissions from the official Discord UI set to ``True``."""
#         return cls(0b1000000000000011111100000000001100000000)

#     @classmethod
#     def stage(cls) -> Self:
#         """A factory method that creates a :class:`Permissions` with all
#         "Stage Channel" permissions from the official Discord UI set to ``True``.

#         .. versionadded:: 1.7
#         """
#         return cls(1 << 32)

#     @classmethod
#     def stage_moderator(cls) -> Self:
#         """A factory method that creates a :class:`Permissions` with all permissions
#         for stage moderators set to ``True``. These permissions are currently:

#         - :attr:`manage_channels`
#         - :attr:`mute_members`
#         - :attr:`move_members`

#         .. versionadded:: 1.7

#         .. versionchanged:: 2.0
#             Added :attr:`manage_channels` permission and removed :attr:`request_to_speak` permission.
#         """
#         return cls(0b1010000000000000000010000)

#     @classmethod
#     def elevated(cls) -> Self:
#         """A factory method that creates a :class:`Permissions` with all permissions
#         that require 2FA set to ``True``. These permissions are currently:

#         - :attr:`kick_members`
#         - :attr:`ban_members`
#         - :attr:`administrator`
#         - :attr:`manage_channels`
#         - :attr:`manage_guild`
#         - :attr:`manage_messages`
#         - :attr:`manage_roles`
#         - :attr:`manage_webhooks`
#         - :attr:`manage_emojis_and_stickers`
#         - :attr:`manage_threads`
#         - :attr:`moderate_members`

#         .. versionadded:: 2.0
#         """
#         return cls(0b10000010001110000000000000010000000111110)

#     @classmethod
#     def advanced(cls) -> Self:
#         """A factory method that creates a :class:`Permissions` with all
#         "Advanced" permissions from the official Discord UI set to ``True``.

#         .. versionadded:: 1.7
#         """
#         return cls(1 << 3)

#     def update(self, **kwargs: bool) -> None:
#         r"""Bulk updates this permission object.

#         Allows you to set multiple attributes by using keyword
#         arguments. The names must be equivalent to the properties
#         listed. Extraneous key/value pairs will be silently ignored.

#         Parameters
#         ------------
#         \*\*kwargs
#             A list of key/value pairs to bulk update permissions with.
#         """
#         for key, value in kwargs.items():
#             if key in self.VALID_FLAGS:
#                 setattr(self, key, value)

#     def handle_overwrite(self, allow: int, deny: int) -> None:
#         # Basically this is what's happening here.
#         # We have an original bit array, e.g. 1010
#         # Then we have another bit array that is 'denied', e.g. 1111
#         # And then we have the last one which is 'allowed', e.g. 0101
#         # We want original OP denied to end up resulting in
#         # whatever is in denied to be set to 0.
#         # So 1010 OP 1111 -> 0000
#         # Then we take this value and look at the allowed values.
#         # And whatever is allowed is set to 1.
#         # So 0000 OP2 0101 -> 0101
#         # The OP is base  & ~denied.
#         # The OP2 is base | allowed.
#         self.value: int = (self.value & ~deny) | allow

#     @flag_value
#     def create_instant_invite(self) -> int:
#         """:class:`bool`: Returns ``True`` if the user can create instant invites."""
#         return 1 << 0

#     @flag_value
#     def kick_members(self) -> int:
#         """:class:`bool`: Returns ``True`` if the user can kick users from the guild."""
#         return 1 << 1

#     @flag_value
#     def ban_members(self) -> int:
#         """:class:`bool`: Returns ``True`` if a user can ban users from the guild."""
#         return 1 << 2

#     @flag_value
#     def administrator(self) -> int:
#         """:class:`bool`: Returns ``True`` if a user is an administrator. This role overrides all other permissions.

#         This also bypasses all channel-specific overrides.
#         """
#         return 1 << 3

#     @flag_value
#     def manage_channels(self) -> int:
#         """:class:`bool`: Returns ``True`` if a user can edit, delete, or create channels in the guild.

#         This also corresponds to the "Manage Channel" channel-specific override."""
#         return 1 << 4

#     @flag_value
#     def manage_guild(self) -> int:
#         """:class:`bool`: Returns ``True`` if a user can edit guild properties."""
#         return 1 << 5

#     @flag_value
#     def add_reactions(self) -> int:
#         """:class:`bool`: Returns ``True`` if a user can add reactions to messages."""
#         return 1 << 6

#     @flag_value
#     def view_audit_log(self) -> int:
#         """:class:`bool`: Returns ``True`` if a user can view the guild's audit log."""
#         return 1 << 7

#     @flag_value
#     def priority_speaker(self) -> int:
#         """:class:`bool`: Returns ``True`` if a user can be more easily heard while talking."""
#         return 1 << 8

#     @flag_value
#     def stream(self) -> int:
#         """:class:`bool`: Returns ``True`` if a user can stream in a voice channel."""
#         return 1 << 9

#     @flag_value
#     def read_messages(self) -> int:
#         """:class:`bool`: Returns ``True`` if a user can read messages from all or specific text channels."""
#         return 1 << 10

#     @make_permission_alias("read_messages")
#     def view_channel(self) -> int:
#         """:class:`bool`: An alias for :attr:`read_messages`.

#         .. versionadded:: 1.3
#         """
#         return 1 << 10

#     @flag_value
#     def send_messages(self) -> int:
#         """:class:`bool`: Returns ``True`` if a user can send messages from all or specific text channels."""
#         return 1 << 11

#     @flag_value
#     def send_tts_messages(self) -> int:
#         """:class:`bool`: Returns ``True`` if a user can send TTS messages from all or specific text channels."""
#         return 1 << 12

#     @flag_value
#     def manage_messages(self) -> int:
#         """:class:`bool`: Returns ``True`` if a user can delete or pin messages in a text channel.

#         .. note::

#             Note that there are currently no ways to edit other people's messages.
#         """
#         return 1 << 13

#     @flag_value
#     def embed_links(self) -> int:
#         """:class:`bool`: Returns ``True`` if a user's messages will automatically be embedded by Discord."""
#         return 1 << 14

#     @flag_value
#     def attach_files(self) -> int:
#         """:class:`bool`: Returns ``True`` if a user can send files in their messages."""
#         return 1 << 15

#     @flag_value
#     def read_message_history(self) -> int:
#         """:class:`bool`: Returns ``True`` if a user can read a text channel's previous messages."""
#         return 1 << 16

#     @flag_value
#     def mention_everyone(self) -> int:
#         """:class:`bool`: Returns ``True`` if a user's @everyone or @here will mention everyone in the text channel."""
#         return 1 << 17

#     @flag_value
#     def external_emojis(self) -> int:
#         """:class:`bool`: Returns ``True`` if a user can use emojis from other guilds."""
#         return 1 << 18

#     @make_permission_alias("external_emojis")
#     def use_external_emojis(self) -> int:
#         """:class:`bool`: An alias for :attr:`external_emojis`.

#         .. versionadded:: 1.3
#         """
#         return 1 << 18

#     @flag_value
#     def view_guild_insights(self) -> int:
#         """:class:`bool`: Returns ``True`` if a user can view the guild's insights.

#         .. versionadded:: 1.3
#         """
#         return 1 << 19

#     @flag_value
#     def connect(self) -> int:
#         """:class:`bool`: Returns ``True`` if a user can connect to a voice channel."""
#         return 1 << 20

#     @flag_value
#     def speak(self) -> int:
#         """:class:`bool`: Returns ``True`` if a user can speak in a voice channel."""
#         return 1 << 21

#     @flag_value
#     def mute_members(self) -> int:
#         """:class:`bool`: Returns ``True`` if a user can mute other users."""
#         return 1 << 22

#     @flag_value
#     def deafen_members(self) -> int:
#         """:class:`bool`: Returns ``True`` if a user can deafen other users."""
#         return 1 << 23

#     @flag_value
#     def move_members(self) -> int:
#         """:class:`bool`: Returns ``True`` if a user can move users between other voice channels."""
#         return 1 << 24

#     @flag_value
#     def use_voice_activation(self) -> int:
#         """:class:`bool`: Returns ``True`` if a user can use voice activation in voice channels."""
#         return 1 << 25

#     @flag_value
#     def change_nickname(self) -> int:
#         """:class:`bool`: Returns ``True`` if a user can change their nickname in the guild."""
#         return 1 << 26

#     @flag_value
#     def manage_nicknames(self) -> int:
#         """:class:`bool`: Returns ``True`` if a user can change other user's nickname in the guild."""
#         return 1 << 27

#     @flag_value
#     def manage_roles(self) -> int:
#         """:class:`bool`: Returns ``True`` if a user can create or edit roles less than their role's position.

#         This also corresponds to the "Manage Permissions" channel-specific override.
#         """
#         return 1 << 28

#     @make_permission_alias("manage_roles")
#     def manage_permissions(self) -> int:
#         """:class:`bool`: An alias for :attr:`manage_roles`.

#         .. versionadded:: 1.3
#         """
#         return 1 << 28

#     @flag_value
#     def manage_webhooks(self) -> int:
#         """:class:`bool`: Returns ``True`` if a user can create, edit, or delete webhooks."""
#         return 1 << 29

#     @flag_value
#     def manage_emojis(self) -> int:
#         """:class:`bool`: Returns ``True`` if a user can create, edit, or delete emojis."""
#         return 1 << 30

#     @make_permission_alias("manage_emojis")
#     def manage_emojis_and_stickers(self) -> int:
#         """:class:`bool`: An alias for :attr:`manage_emojis`.

#         .. versionadded:: 2.0
#         """
#         return 1 << 30

#     @flag_value
#     def use_application_commands(self) -> int:
#         """:class:`bool`: Returns ``True`` if a user can use slash commands.

#         .. versionadded:: 1.7
#         """
#         return 1 << 31

#     @flag_value
#     def request_to_speak(self) -> int:
#         """:class:`bool`: Returns ``True`` if a user can request to speak in a stage channel.

#         .. versionadded:: 1.7
#         """
#         return 1 << 32

#     @flag_value
#     def manage_events(self) -> int:
#         """:class:`bool`: Returns ``True`` if a user can manage guild events.

#         .. versionadded:: 2.0
#         """
#         return 1 << 33

#     @flag_value
#     def manage_threads(self) -> int:
#         """:class:`bool`: Returns ``True`` if a user can manage threads.

#         .. versionadded:: 2.0
#         """
#         return 1 << 34

#     @flag_value
#     def create_public_threads(self) -> int:
#         """:class:`bool`: Returns ``True`` if a user can create public threads.

#         .. versionadded:: 2.0
#         """
#         return 1 << 35

#     @flag_value
#     def create_private_threads(self) -> int:
#         """:class:`bool`: Returns ``True`` if a user can create private threads.

#         .. versionadded:: 2.0
#         """
#         return 1 << 36

#     @flag_value
#     def external_stickers(self) -> int:
#         """:class:`bool`: Returns ``True`` if a user can use stickers from other guilds.

#         .. versionadded:: 2.0
#         """
#         return 1 << 37

#     @make_permission_alias("external_stickers")
#     def use_external_stickers(self) -> int:
#         """:class:`bool`: An alias for :attr:`external_stickers`.

#         .. versionadded:: 2.0
#         """
#         return 1 << 37

#     @flag_value
#     def send_messages_in_threads(self) -> int:
#         """:class:`bool`: Returns ``True`` if a user can send messages in threads.

#         .. versionadded:: 2.0
#         """
#         return 1 << 38

#     @flag_value
#     def use_embedded_activities(self) -> int:
#         """:class:`bool`: Returns ``True`` if a user can launch an embedded application in a Voice channel.

#         .. versionadded:: 2.0
#         """
#         return 1 << 39

#     @flag_value
#     def moderate_members(self) -> int:
#         """:class:`bool`: Returns ``True`` if a user can time out other members.

#         .. versionadded:: 2.0
#         """
#         return 1 << 40
