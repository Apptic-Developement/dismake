from __future__ import annotations

from typing import Any, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..types import AsyncFunction

__all__ = ("_BaseAppCommand",)


class _BaseAppCommand:
    def __init__(
        self,
        name: str,
        description: str,
        name_localizations: Optional[dict[str, str]],
        description_localizations: Optional[dict[str, str]],
    ) -> None:
        self.name = name
        self.description = description
        self.name_localizations = name_localizations
        self.description_localizations = description_localizations

    def to_dict(self) -> dict[str, Any]:
        base: dict[str, Any] = {
            "name": self.name,
            "description": self.description,
        }
        if self.name_localizations is not None:
            base["name_localizations"] = self.name_localizations
        if self.description_localizations is not None:
            base["description_localizations"] = self.description_localizations
        return base
