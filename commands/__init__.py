from __future__ import annotations

from typing import TYPE_CHECKING

from .autocomplete import Autocomplete
from .info import InfoCommand
from .components import Component
from .nested import NestedCommand

if TYPE_CHECKING:
    from dismake import Bot


def get_commands(bot: Bot):
    return [Autocomplete(bot), InfoCommand(bot), Component(bot), NestedCommand(bot)]
