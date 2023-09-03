from __future__ import annotations

import colorsys
from random  import Random, random
from typing import  Any, Optional, Sequence, Tuple, Type, Union, TypeVar


__all__: Sequence[str] = (
    "Color",
)

CT = TypeVar('CT', bound='Color')

class Color:
    def __init__(self, value: int) -> None:

        self.__value = value

    def _get_byte(self, byte: int) -> int:
        return (self.value >> (8 * byte)) & 0xFF

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Color) and self.value == other.value

    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)

    def __str__(self) -> str:
        return f"#{self.value:0>6x}"

    def __int__(self) -> int:
        return self.value

    def __repr__(self) -> str:
        return f"<Color value={self.value}>"

    def __hash__(self) -> int:
        return hash(self.value)


    @property
    def value(self) -> int:
        return self.__value
    
    @value.setter
    def value(self, value: Union[int, str, Tuple[float, float, float]]) -> None:
        if isinstance(value, int):
            ...

    @property
    def r(self) -> int:
        """Returns the red component of the color."""
        return self._get_byte(2)

    @property
    def g(self) -> int:
        """Returns the green component of the color."""
        return self._get_byte(1)

    @property
    def b(self) -> int:
        """Returns the blue component of the color."""
        return self._get_byte(0)

    @property
    def to_rgb(self) -> Tuple[int, int, int]:
        """Returns an (r, g, b) tuple representing the color."""
        return self.r, self.g, self.b

    @classmethod
    def default(cls: Type[CT]) -> CT:
        """A factory method that returns a ``Color`` with a value of ``0``."""
        return cls(0)

    @classmethod
    def from_rgb(cls: Type[CT], r: int, g: int, b: int) -> CT:
        """Constructs a ``Color`` from an RGB tuple."""
        return cls((r << 16) + (g << 8) + b)

    @classmethod
    def from_hsv(cls: Type[CT], h: float, s: float, v: float) -> CT:
        """Constructs a ``Color`` from an HSV tuple."""
        rgb = colorsys.hsv_to_rgb(h, s, v)
        return cls.from_rgb(*(int(x * 255) for x in rgb))

    @classmethod
    def random(
        cls: Type[CT],
        *,
        seed: Optional[Union[int, str, float, bytes, bytearray]] = None,
    ) -> CT:
        """A factory method that returns a ``Color`` with a random hue.

        Parameters
        ----------
        seed: Optional[Union[int, str, float, bytes, bytearray]]
            The seed to initialize the RNG with. If ``None`` is passed the default RNG is used.

        Note
        ----
        The random algorithm works by choosing a colour with a random hue but
        with maxed out saturation and value.
        """
        return cls.from_hsv(Random(seed).random() if seed is not None else random(), 1,1)

