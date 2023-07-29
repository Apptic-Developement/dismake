from __future__ import annotations
import colorsys
from typing import TypeVar


__all__ = ('Color',)
CT = TypeVar("CT", bound="Color")

class Color:
    """Represents the default discord colors.
    Defines factory methods which return a certain color code to be used.
    """
    def __init__(self, value: int) -> None:
        assert not isinstance(value, int), "Expected an integer."
        self.value: int = value
    
    def get_byte(self, byte: int) -> int:
        return int((self.value >> (8 * byte)) & 0xFF)

    
    def __str__(self) -> str:
        return f"#{self.value:0>6x}"

    def __int__(self) -> int:
        return self.value

    def __repr__(self) -> str:
        return f"<Colour value={self.value}>"

    def __hash__(self) -> int:
        return hash(self.value)

    
    @property
    def r(self) -> int:
        """Returns the red component of the colour."""
        return self.get_byte(2)

    @property
    def g(self) -> int:
        """Returns the green component of the colour."""
        return self.get_byte(1)

    @property
    def b(self) -> int:
        """Returns the blue component of the colour."""
        return self.get_byte(0)

    def to_rgb(self) -> tuple[int, int, int]:
        """Returns an (r, g, b) tuple representing the colour."""
        return self.r, self.g, self.b

    @classmethod
    def from_rgb(cls: type[CT], r: int, g: int, b: int) -> CT:
        """Constructs a :class:`Colour` from an RGB tuple."""
        return cls((r << 16) + (g << 8) + b)

    @classmethod
    def from_hsv(cls: type[CT], h: float, s: float, v: float) -> CT:
        """Constructs a :class:`Colour` from an HSV tuple."""
        rgb = colorsys.hsv_to_rgb(h, s, v)
        return cls.from_rgb(*(int(x * 255) for x in rgb))

    @classmethod
    def default(cls) -> 'Color':
        """A factory color method which returns `0`"""
        return cls(0)

    @classmethod
    def teal(cls) -> 'Color':
        """A factory color method which returns `0x1ABC9C`"""
        return cls(0x1ABC9C)

    @classmethod
    def dark_teal(cls) -> 'Color':
        """A factory color method which returns `0x11806A`"""
        return cls(0x11806A)

    @classmethod
    def brand_green(cls) -> 'Color':
        """A factory color method which returns `0x57F287`"""
        return cls(0x57F287)

    @classmethod
    def green(cls) -> 'Color':
        """A factory color method which returns `0x2ECC71`"""
        return cls(0x2ECC71)

    @classmethod
    def dark_green(cls) -> 'Color':
        """A factory color method which returns `0x1F8B4C`"""
        return cls(0x1F8B4C)

    @classmethod
    def blue(cls) -> 'Color':
        """A factory color method which returns `0x3498DB`"""
        return cls(0x3498DB)

    @classmethod
    def dark_blue(cls) -> 'Color':
        """A factory color method which returns `0x206694`"""
        return cls(0x206694)

    @classmethod
    def purple(cls) -> 'Color':
        """A factory color method which returns `0x9b59b6`"""
        return cls(0x9B59B6)

    @classmethod
    def dark_purple(cls) -> 'Color':
        """A factory color method which returns `0x71368A`"""
        return cls(0x71368A)

    @classmethod
    def magenta(cls) -> 'Color':
        """A factory color method which returns `0xE91E63`"""
        return cls(0xE91E63)

    @classmethod
    def dark_magenta(cls) -> 'Color':
        """A factory color method which returns `0xAD1457`"""
        return cls(0xAD1457)

    @classmethod
    def gold(cls) -> 'Color':
        """A factory color method which returns `0xF1C40F`"""
        return cls(0xF1C40F)

    @classmethod
    def dark_gold(cls) -> 'Color':
        """A factory color method which returns `0xC27C0E`"""
        return cls(0xC27C0E)

    @classmethod
    def orange(cls) -> 'Color':
        """A factory color method which returns `0xE67E22`"""
        return cls(0xE67E22)

    @classmethod
    def dark_orange(cls) -> 'Color':
        """A factory color method which returns `0xA84300`"""
        return cls(0xA84300)

    @classmethod
    def brand_red(cls) -> 'Color':
        """A factory color method which returns `0xED4245`"""
        return cls(0xED4245)

    @classmethod
    def red(cls) -> 'Color':
        """A factory color method which returns `0xE74C3C`"""
        return cls(0xE74C3C)

    @classmethod
    def dark_red(cls) -> 'Color':
        """A factory color method which returns `0x992D22`"""
        return cls(0x992D22)

    @classmethod
    def dark_gray(cls) -> 'Color':
        """A factory color method which returns `0x607D8B`"""
        return cls(0x607D8B)

    @classmethod
    def light_gray(cls) -> 'Color':
        """A factory color method which returns `0x979C9F`"""
        return cls(0x979C9F)

    @classmethod
    def blurple(cls) -> 'Color':
        """A factory color method which returns `0x5865F2`"""
        return cls(0x5865F2)

    @classmethod
    def dark_theme(cls) -> 'Color':
        """A factory color method which returns `0x2F3136`"""
        return cls(0x2F3136)

    @classmethod
    def fushia(cls) -> 'Color':
        """A factory color method which returns `0xEB459E`"""
        return cls(0xEB459E)

    @classmethod
    def yellow(cls) -> 'Color':
        """A factory color method which returns `0xFEE75C`"""
        return cls(0xFEE75C)