from __future__ import annotations
from typing import Any, List, Optional

from .ui import House
from .enums import MessageFlags
from .errors import HouseError


def handle_send_params(
    content: str,
    *,
    tts: Optional[bool] = None,
    embeds: Optional[list] = None,
    allowed_mentions: Optional[Any] = None,
    houses: Optional[List[House]] = None,
    attachments: Optional[List[Any]] = None,
    embed: Optional[Any] = None,
    ephemeral: bool = False,
):
    payload: dict[str, Any] = {"content": content}
    if ephemeral:
        payload.update({"flags": MessageFlags.EPHEMERAL.value})
    if tts:
        payload.update({"tts": tts})
    if houses:
        if len(houses) > 5:
            raise HouseError("A message can only have 5 houses.")
        payload.update({"components": [house.to_dict() for house in houses]})
    _embeds = list()
    if embeds:
        for emb in embeds:
            _embeds.append(emb)
    if embed:
        _embeds.append(embed)

    if _embeds:
        embeds = _embeds
    # TODO: attachments, components, allowed_mentions
    return payload
