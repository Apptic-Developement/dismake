from __future__ import annotations

import attrs
import typing

from .user import User

# if typing.TYPE_CHECKING:
#     from dismake import Client
#     from typing_extensions import Self
#     from dismake.types import MemberData, Snowflake
#     from datetime import datetime


__all__: typing.Sequence[str] = ("Member",)


@attrs.define(kw_only=True, hash=True, weakref_slot=False)
class Member(User):
    """Represents a guild member."""

    # TODO