from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Generic, List, Optional

if TYPE_CHECKING:
    from typing_extensions import Self

    from ..enums import ApplicationCommandOptionType, ApplicationCommandType, Locale
    from ..models import Permissions
    from ..types import AsyncFunction, ClientT
    from .group import Group
    from .parameter import Option

__all__ = ("Command",)


class Command(Generic[ClientT]):
    def __init__(
        self,
        callback: AsyncFunction,
        client: ClientT,
        name: str,
        description: str,
        options: Optional[List[Option]] = None,
        name_localizations: Optional[Dict[Locale, str]] = None,
        description_localizations: Optional[Dict[Locale, str]] = None,
        default_member_permissions: Optional[Permissions] = None,
        guild_only: Optional[bool] = None,
        guild_id: Optional[int] = None,
        nsfw: Optional[bool] = None,
        parent: Optional[Group[ClientT]] = None,
    ) -> None:
        self.client = client
        self.name = name
        self.description = description
        self.options = options
        self.name_localizations = name_localizations
        self.description_localizations = description_localizations
        self.default_member_permissions = default_member_permissions
        self.guild_only = guild_only
        self.guild_id = guild_id
        self.nsfw = nsfw
        self.callback = callback
        self.parent = parent
        self.type = (
            ApplicationCommandType.CHAT_INPUT
            if parent is None
            else ApplicationCommandOptionType.SUB_COMMAND
        )

    async def fetch(self) -> Self:
        return NotImplemented
    
    def to_dict(self) -> Dict[str, Any]:
        base: Dict[str, Any] = {
            "type": self.type.value,
            "name": self.name,
            "description": self.description,
        }

        if self.options is not None:
            base["options"] = [x.to_dict() for x in self.options]
        if self.name_localizations is not None:
            base["name_localizations"] = {
                k.value: v for k, v in self.name_localizations.items()
            }
        if self.description_localizations is not None:
            base["description_localizations"] = {
                k.value: v for k, v in self.description_localizations.items()
            }
        if self.default_member_permissions is not None:
            base["default_member_permissions"] = self.default_member_permissions
        if self.guild_only is not None:
            base["dm_permission"] = not self.guild_only
        if self.guild_id is not None:
            base["guild_id"] = self.guild_id
        if self.nsfw is not None:
            base["nsfw"] = self.nsfw
        return base
