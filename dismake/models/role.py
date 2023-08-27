from __future__ import annotations

import typing
import attrs

from .permissions import Permissions

if typing.TYPE_CHECKING:
    from dismake import Client
    from typing_extensions import Self
    from dismake.types import Snowflake
    from discord_typings import RoleData

__all__: typing.Sequence[str] = ("PartialRole", "Role")


@attrs.define(kw_only=True, hash=True, weakref_slot=False)
class PartialRole:
    """Represents a partial guild bound role object."""

    client: Client = attrs.field(repr=False, eq=False, hash=False)
    """Client application that models may use for procedures."""

    id: Snowflake = attrs.field(hash=True)
    """The ID of this entity."""

    @property
    def mention(self) -> str:
        """Return a raw mention string for the role."""
        return f"<@&{self.id}>"


@attrs.define(kw_only=True, hash=True, weakref_slot=False)
class Role(PartialRole):
    name: str = attrs.field(eq=False, hash=False, repr=True)
    """The role's name."""

    color: int = attrs.field(eq=False, hash=False, repr=True)
    """The color of this Role."""

    guild_id: Snowflake = attrs.field(eq=False, hash=False, repr=True)
    """The ID of the guild this role belongs to."""

    is_hoisted: bool = attrs.field(eq=False, hash=False, repr=True)
    """Whether this role is hoisting the members it's attached to in the member list."""

    icon_hash: typing.Optional[str] = attrs.field(eq=False, hash=False, repr=False)
    """Hash of the role's icon if set, else `None`."""

    unicode_emoji: typing.Any = attrs.field(eq=False, hash=False, repr=False)
    """Role's icon as an unicode emoji if set, else `None`."""

    position: int = attrs.field(eq=False, hash=False, repr=True)
    """The position of this role in the role hierarchy."""

    permissions: Permissions = attrs.field(eq=False, hash=False, repr=False)
    """The guild wide permissions this role gives to the members it's attached to."""

    is_managed: bool = attrs.field(eq=False, hash=False, repr=False)
    """Whether this role is managed by an integration."""

    is_mentionable: bool = attrs.field(eq=False, hash=False, repr=True)
    """Whether this role can be mentioned by all regardless of permissions."""

    bot_id: typing.Optional[Snowflake] = attrs.field(eq=False, hash=False, repr=True)
    """The ID of the bot this role belongs to.

    If `None`, this is not a bot role.
    """

    integration_id: typing.Optional[Snowflake] = attrs.field(
        eq=False, hash=False, repr=True
    )
    """The ID of the integration this role belongs to.

    If `None`, this is not a integration role.
    """

    is_premium_subscriber: bool = attrs.field(eq=False, hash=False, repr=True)
    """Whether this role is the guild's nitro subscriber role."""

    subscription_listing_id: typing.Optional[Snowflake] = attrs.field(
        eq=False, hash=False, repr=True
    )
    """The ID of this role's subscription SKU and listing.

    If `None`, this is not a purchasable role.
    """

    is_available_for_purchase: bool = attrs.field(eq=False, hash=False, repr=True)
    """Whether this role is available for purchase."""

    is_guild_linked_role: bool = attrs.field(eq=False, hash=False, repr=True)
    """Whether this role is a linked role in the guild."""

    def __str__(self) -> str:
        return self.name

    @property
    def colour(self) -> typing.Any:
        return self.color

    @property
    def mention(self) -> str:
        """Return a raw mention string for the role.

        When this role represents @everyone mentions will only work if
        `mentions_everyone` is `True`.
        """
        if self.guild_id == self.id:
            return "@everyone"

        return super().mention

    @classmethod
    def from_revived_data(
        cls, client: Client, guild_id: Snowflake, data: RoleData
    ) -> Self:
        tags = data.get("tags", {})
        return cls(
            client=client,
            id=data["id"],
            name=data["name"],
            guild_id=guild_id,
            color=data["color"],
            is_hoisted=data["hoist"],
            is_mentionable=data["mentionable"],
            is_managed=data["managed"],
            icon_hash=data.get("icon"),
            unicode_emoji=data.get("unicode_emoji"),
            position=data["position"],
            permissions=Permissions(int(data.get("permissions", 0))),
            bot_id=tags.get("bot_id"),
            integration_id=tags.get("integration_id"),
            is_premium_subscriber=tags.get("premium_subscriber") or False,
            subscription_listing_id=tags.get("subscription_listing_id") or False,
            is_available_for_purchase=tags.get("available_for_purchase") or False,
            is_guild_linked_role=tags.get("guild_connections") or False,
        )
