from __future__ import annotations

from typing import TYPE_CHECKING, Sequence

if TYPE_CHECKING:
    from typing_extensions import Self
    from ..types import EmbedData

__all__: Sequence[str] = ("Embed",)


class Embed:
    """Represents an discord embed."""

    def __init__(self) -> None:
        pass

    @classmethod
    def from_dict(cls, data: EmbedData) -> Self:
        raise NotImplementedError
