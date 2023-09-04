from __future__ import annotations

from typing import TYPE_CHECKING, Sequence

if TYPE_CHECKING:
    ...

__all__: Sequence[str] = ("DismakeException",)


class DismakeException(Exception):
    ...
