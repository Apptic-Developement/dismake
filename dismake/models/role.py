from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Optional, Sequence, Union


from .color import Color
from .permissions import Permissions
from .asset import Asset
from ..utils import snowflake_time

if TYPE_CHECKING:
    from dismake import Client
    from datetime import datetime
    from ..types import RoleData, RoleTagsData

__all__: Sequence[str] = ("PartialRole", "Role")


class PartialRole:
    """Represents a Partial Role

    Parameters
    ----------
    client: Client
        The client application that models may use for procedures.
    id: int
        The unique ID of the role.

    Attributes
    ----------
    client: Client
        The client application that models may use for procedures.
    id: int
        The unique ID of the role.
    """

    def __init__(self, client: Client, id: int) -> None:
        self.client = client
        self.id = id

    @property
    def mention(self) -> str:
        """Return a raw mention string for the role."""
        return f"<&@{self.id}>"


class Role(PartialRole):
    """Represents a Role.

    Parameters
    ----------
    client: Client
        The client application that models may use for procedures.
    data: RoleData
        The data payload containing role information.

    Attributes
    ----------
    name: str
        The name of the role.
    color: int
        The color code of the role.
    hoist: bool
        Whether the role is hoisted.
    unicode_emoji: Optional[str]
        The Unicode emoji associated with the role.
    position: int
        The position of the role.
    permissions: Permissions
        The permissions granted to the role.
    managed: bool
        Whether the role is managed.
    mentionable: bool
        Whether the role is mentionable.

    Operations
    ----------
    - ``x == y``:
        Checks if two roles are equal.

    - ``x != y``:
        Checks if two roles are not equal.

    - ``str(x)``:
        Returns the role's name.

    """

    def __init__(self, client: Client, data: RoleData) -> None:
        super().__init__(client=client, id=int(data["id"]))
        self.name: str = data["name"]
        self.color: Color = Color(data["color"])
        self.hoist: bool = data["hoist"]
        self._icon: Optional[str] = data.get("icon")
        self.unicode_emoji: Optional[str] = data.get("unicode_emoji")
        self.position: int = data["position"]
        self.permissions: Permissions = Permissions(int(data["permissions"]))
        self.managed: bool = data["managed"]
        self.mentionable: bool = data["mentionable"]
        self.guild_id: int
        # self.flags: int = data["flags"]
        self._tags: Union[RoleTagsData, Dict[Any, Any]] = data.get("tags") or {}

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Role) and self.id == other.id

    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)

    def __str__(self) -> str:
        return f"Role(id={self.id}, name={self.name})"

    @property
    def created_at(self) -> datetime:
        """Returns the role's creation time in UTC."""
        return snowflake_time(self.id)

    @property
    def icon(self) -> Optional[Asset]:
        """Returns the role's icon asset, if available.

        If this is ``None``, the role might instead have unicode emoji as its icon
        If you want the icon that a role has displayed, consider using ``Role.display_icon``.
        """
        return (
            Asset.from_icon(self.id, self._icon, path="role")
            if self._icon is not None
            else None
        )

    @property
    def display_icon(self) -> Optional[Union[Asset, str]]:
        """Returns the role's display icon, if available."""
        return self.icon or self.unicode_emoji

    @property
    def bot_id(self) -> Optional[int]:
        """The ID of the bot this role belongs to."""
        bot_id = self._tags.get("bot_id")
        return int(bot_id) if bot_id is not None else None

    @property
    def integration_id(self) -> Optional[int]:
        """The ID of the integration this role belongs to."""
        integration_id = self._tags.get("integration_id")
        return int(integration_id) if integration_id is not None else None

    @property
    def is_premium_subscriber(self) -> bool:
        """Whether this role is the guild's nitro subscriber role."""
        return "premium_subscriber" in self._tags

    @property
    def is_available_for_purchase(self) -> bool:
        """Whether this role is available for purchase."""
        return "available_for_purchase" in self._tags

    @property
    def is_guild_linked_role(self) -> bool:
        """Whether this role is a linked role in the guild."""
        return "guild_connections" in self._tags

    @property
    def subscription_listing_id(self) -> Optional[int]:
        """The ID of this role's subscription SKU and listing."""
        subscription_listing_id = self._tags.get("subscription_listing_id")
        return (
            int(subscription_listing_id)
            if subscription_listing_id is not None
            else None
        )
