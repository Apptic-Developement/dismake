from __future__ import annotations

__all__ = ("UndefinedType", "Undefined")


class UndefinedType:
    """
    Represents an undefined value.

    An instance of this class can be used to represent an undefined value,
    useful in cases where you need to distinguish between a value being explicitly set and not set.

    Example
    -------
        >>> from dismake import UndefinedType, Undefined
        >>> value: UndefinedType = Undefined  # Assign the value to be undefined
        ...
        >>> if value is Undefined:
        ...     print("The value is undefined.")
        >>> else:
        ...     print(f"The value is {value}.")

    """

    _instance = None

    def __new__(cls) -> UndefinedType:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __repr__(self) -> str:
        return "Undefined"

    def __bool__(self) -> bool:
        return False

    def __eq__(self, other: object) -> bool:
        """
        Compare an `Undefined` object with another object.

        `Undefined` always compares as not equal to any other object,
        including another `Undefined` object

        Parameters
        ---------
            other: The object to compare with.

        Returns
        -------
            True if `other` is not an instance of `Undefined`, False otherwise.

        """
        return not isinstance(other, UndefinedType)


Undefined = UndefinedType()
