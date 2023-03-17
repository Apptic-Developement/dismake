from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    from typing_extensions import TypeVar
    from .client import Bot
    ClientT = TypeVar("ClientT", bound=Bot, covariant=True, default=Bot)

else:
    ClientT = TypeVar("ClientT", bound="Bot", covariant=True)