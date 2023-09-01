from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, Coroutine, Sequence, TypeVar


__all__: Sequence[str] = ("ClientT", "AsyncFunction")


if TYPE_CHECKING:
    from ..client import Client
    
    ClientT = TypeVar("ClientT", covariant=True, bound=Client)
else:
    ClientT = TypeVar("ClientT", covariant=True)

AsyncFunction = Callable[..., Coroutine[Any, Any, Any]]