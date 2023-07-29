from __future__ import annotations
from enum import IntFlag

__all__ = ("RoleFlags",)


class RoleFlags(IntFlag):
    IN_PROMPT = 1 << 0
