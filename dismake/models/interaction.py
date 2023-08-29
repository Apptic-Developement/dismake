from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from dismake import Client


__all__: typing.Sequence[str] = (
    "Interaction",
)

ClientT = typing.TypeVar("ClientT", bound="Client")

class Interaction(typing.Generic[ClientT]):
    def __init__(self) -> None:
        pass