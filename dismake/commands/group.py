from __future__ import annotations

from typing import TYPE_CHECKING, Generic

if TYPE_CHECKING:
    from ..types import ClientT

__all__ = ("Group",)


class Group(Generic[ClientT]):
    def __init__(self) -> None:
        pass
