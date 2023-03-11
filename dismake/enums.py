from __future__ import annotations

from enum import Enum

__all__ = (
    "DefaultAvatar",
)

class DefaultAvatar(Enum):
    blurple = 0
    grey = 1
    gray = 1
    green = 2
    orange = 3
    red = 4

    def __str__(self) -> str:
        return self.name