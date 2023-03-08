from __future__ import annotations
from typing import Callable
import re

from .types.command import SubCommandDict

__all__ = (
    "SlashCommand",
)



def validate_name(name: str):
    SLASH_COMMAND_NAME_REGEX = r'^[-_\p{L}\p{N}\p{sc=Deva}\p{sc=Thai}]{1,32}$'
    if re.match(SLASH_COMMAND_NAME_REGEX, name, re.UNICODE):
        return name
    raise ValueError()


class SlashCommand:
    def __init__(
        self,
        name: str,
        *,
        description: str = "No description provided."
    ) -> None:
        self._name = validate_name(name)
        self._description = description
        self.subcommands: list[SubCommandDict | None] = []

    def add_subcommand(self, name: str, description: str, callback: Callable) -> None:
        self.subcommands.append(
            {
                "name": name, "description": description, "callback": callback
            }
        )

    async def callback(self, interaction):
        pass