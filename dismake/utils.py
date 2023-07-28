from __future__ import annotations
from typing import Any, Optional


__all__ = (
    "get_as_snowflake",
)

def get_as_snowflake(data: Any, key: str) -> Optional[int]:
    try:
        value = data[key]
    except KeyError:
        return None
    else:
        return value and int(value)