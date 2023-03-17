from __future__ import annotations
from typing import Union

__all__ = ("SnowFlake", "SnowFlakeL")

SnowFlake = Union[str, int]
SnowFlakeL = list[Union[str, int]]
