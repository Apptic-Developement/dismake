from __future__ import annotations

from typing import TYPE_CHECKING, Any, Sequence

if TYPE_CHECKING:
    ...

__all__: Sequence[str] = ("Option", "Parameter", "P")


class Option:
    def __init__(self) -> None:
        pass


def Parameter(*args: Any, **kwargs: Any) -> Any:
    return Option(*args, **kwargs)


P = Parameter
