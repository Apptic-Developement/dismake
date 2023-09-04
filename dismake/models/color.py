# Credit to discord.py

from __future__ import annotations

import colorsys
import re
from random import Random, random
from typing import Any, Optional, Sequence, Tuple, Type, TypeVar, Union

__all__: Sequence[str] = ("Color",)

CT = TypeVar("CT", bound="Color")


RGB_REGEX = re.compile(
    r"rgb\s*\((?P<r>[0-9.]+%?)\s*,\s*(?P<g>[0-9.]+%?)\s*,\s*(?P<b>[0-9.]+%?)\s*\)"
)


def parse_hex_number(argument: str) -> Color:
    arg = "".join(i * 2 for i in argument) if len(argument) == 3 else argument
    try:
        value = int(arg, base=16)
        if not (0 <= value <= 0xFFFFFF):
            raise ValueError("hex number out of range for 24-bit colour")
    except ValueError:
        raise ValueError("invalid hex digit given") from None
    else:
        return Color(value=value)


def parse_rgb_number(number: str) -> int:
    if number[-1] == "%":
        value = float(number[:-1])
        if not (0 <= value <= 100):
            raise ValueError("rgb percentage can only be between 0 to 100")
        return round(255 * (value / 100))

    value = int(number)
    if not (0 <= value <= 255):
        raise ValueError("rgb number can only be between 0 to 255")
    return value


def parse_rgb(argument: str, *, regex: re.Pattern[str] = RGB_REGEX) -> Color:
    match = regex.match(argument)
    if match is None:
        raise ValueError("invalid rgb syntax found")

    red = parse_rgb_number(match.group("r"))
    green = parse_rgb_number(match.group("g"))
    blue = parse_rgb_number(match.group("b"))
    return Color.from_rgb(red, green, blue)


class Color:
    """Represents a Discord role colour. This class is similar
    to a (red, green, blue).

    There is an alias for this called Colour.
    Attributes
    ----------
    value: int
        The raw integer color value.

    Operations
    ----------
    - ``x == y``:
        Checks if two colors are equal.

    - ``x != y``:
        Checks if two colors are not equal.

    - ``str(x)``:
        Returns the hex format for the colour.

    - ``hash(x)``:
        Return the color's hash.

    - ``int(x)``:
        Returns the raw color value.
    """

    def __init__(self, value: int) -> None:
        self.value = value

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
        return cls.from_hsv(
            Random(seed).random() if seed is not None else random(), 1, 1
        )

    @classmethod
    def from_str(cls, value: str) -> "Color":
        """Constructs a ``Color`` from a string.

        The following formats are accepted:

        - ``0x<hex>``
        - ``#<hex>``
        - ``0x#<hex>``
        - ``rgb(<number>, <number>, <number>)``

        Like CSS, ``<number>`` can be either 0-255 or 0-100% and ``<hex>`` can be
        either a 6 digit hex number or a 3 digit hex shortcut (e.g. #FFF).

        Raises
        -------
        ValueError
            The string could not be converted into a color.
        """

        if value[0] == "#":
            return parse_hex_number(value[1:])

        if value[0:2] == "0x":
            rest = value[2:]
            # Legacy backwards compatible syntax
            if rest.startswith("#"):
                return parse_hex_number(rest[1:])
            return parse_hex_number(rest)

        arg = value.lower()
        if arg[0:3] == "rgb":
            return parse_rgb(arg)

        raise ValueError("unknown colour format given")
