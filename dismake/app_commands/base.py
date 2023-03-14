from __future__ import annotations
import re
from typing import Optional

from pydantic import BaseModel, validator

__all__ = (
    "BaseSlashCommand",
)

THAI_COMBINING = r"\u0e31-\u0e3a\u0e47-\u0e4e"
DEVANAGARI_COMBINING = r"\u0900-\u0903\u093a\u093b\u093c\u093e\u093f\u0940-\u094f\u0955\u0956\u0957\u0962\u0963"
VALID_SLASH_COMMAND_NAME = re.compile(
    r"^[-_\w" + THAI_COMBINING + DEVANAGARI_COMBINING + r"]{1,32}$"
)

class BaseSlashCommand(BaseModel):
    type: int
    name: str
    name_localizations: Optional[str] = None
    description: str
    description_localizations: Optional[str] = None

    @validator("name")
    def validate_name(cls, value: str):
        if VALID_SLASH_COMMAND_NAME.match(value) is None:
            raise NameError(
                f"{value!r} must be between 1-32 characters and contain only lower-case letters, numbers, hyphens, or underscores."
            )
        return value