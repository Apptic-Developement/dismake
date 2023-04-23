from __future__ import annotations
from typing import Any, Dict, List, Optional, Union

from .ui import House
from .enums import MessageFlags


def handle_send_params(
    content: str,
    *,
    tts: Optional[bool] = None,
    embeds: Optional[list] = None,
    allowed_mentions: Optional[Any] = None,
    house: Optional[Union[House, Dict[Any, Any]]] = None,
    attachments: Optional[List[Any]] = None,
    embed: Optional[Any] = None,
    ephemeral: bool = False,
):
    payload: dict[str, Any] = {"content": content}
    if ephemeral:
        payload.update({"flags": MessageFlags.EPHEMERAL.value})
    if tts:
        payload.update({"tts": tts})
    if house:
        if isinstance(house, House):
            payload.update({"components": house.to_dict()})
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

def  handle_edit_params(
    content: str,
    *,
    tts: Optional[bool] = None,
    embeds: Optional[list] = None,
    allowed_mentions: Optional[Any] = None,
    houses: Optional[List[House]] = None,
    attachments: Optional[List[Any]] = None,
    embed: Optional[Any] = None,
) -> Dict[str, Any]:
    payload: Dict[str, Any] = {"content": content}
    if tts:
        payload.update({"tts": tts})
    embs = list()
    if embeds:
        for embed in embeds:
            embs.append(embed)
    if embed:
        embs.append(embed)
    
    if embeds:
        embeds = embs
    
    if houses:
        payload.update({"components": [house.to_dict() for house in houses]})
    else:
        payload.update({"components": None})
    return payload