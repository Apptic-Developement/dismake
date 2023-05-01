from __future__ import annotations


__all__ = ("UndefinedType", "UNDEFINED")


class UndefinedType:
    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        return "Undefined"


UNDEFINED = UndefinedType
