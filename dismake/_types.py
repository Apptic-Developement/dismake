from __future__ import annotations

from typing import Optional
from pydantic import BaseModel


class Locale(BaseModel):
    id: Optional[str]
    da: Optional[str]
    de: Optional[str]
    en_GB: Optional[str]
    en_US: Optional[str]
    es_ES: Optional[str]
    fr: Optional[str]
    hr: Optional[str]
    it: Optional[str]
    lt: Optional[str]
    hu: Optional[str]
    nl: Optional[str]
    no: Optional[str]
    pl: Optional[str]
    pt_BR: Optional[str]
    ro: Optional[str]
    fi: Optional[str]
    sv_SE: Optional[str]
    vi: Optional[str]
    tr: Optional[str]
    cs: Optional[str]
    el: Optional[str]
    bg: Optional[str]
    ru: Optional[str]
    uk: Optional[str]
    hi: Optional[str]
    th: Optional[str]
    zh_CN: Optional[str]
    ja: Optional[str]
    zh_TW: Optional[str]
    ko: Optional[str]
