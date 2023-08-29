from __future__ import annotations

import typing
import attrs

__all__: typing.Sequence[str] = (
    "PartialMessage",
    "Message",
)

@attrs.define(kw_only=True, hash=True, weakref_slot=True)
class PartialMessage:
    """Represent a discord partial message"""

@attrs.define(kw_only=True, hash=True, weakref_slot=True)
class Message(PartialMessage):
    """Represent a discord message"""