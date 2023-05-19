from __future__ import annotations
from typing import Any, Dict, List, Optional, TYPE_CHECKING, Union


from .enums import MessageFlags

if TYPE_CHECKING:
    from .models import Embed
    from .ui import View


__all__ = ("handle_send_params", "handle_edit_params")


def handle_send_params(
    content: str,
    *,
    tts: Optional[bool] = None,
    embeds: Optional[list[Embed]] = None,
    allowed_mentions: Optional[Any] = None,
    view: Optional[Union[View, Dict[Any, Any]]] = None,
    attachments: Optional[List[Any]] = None,
    embed: Optional[Any] = None,
    ephemeral: bool = False,
) -> dict[str, Any]:
    payload: dict[str, Any] = {"content": content}
    if ephemeral:
        payload.update({"flags": MessageFlags.EPHEMERAL.value})
    if tts:
        payload.update({"tts": tts})
    if view:
        if isinstance(view, dict):
            payload.update({"components": view})
        else:
            payload.update({"components": view.to_dict()})
    _embeds: list[Embed] = list()
    if embeds:
        for emb in embeds:
            _embeds.append(emb)
    if embed:
        _embeds.append(embed)

    if _embeds:
        embeds = _embeds
    return payload


def handle_edit_params(
    content: str,
    *,
    tts: Optional[bool] = None,
    embeds: Optional[list[Embed]] = None,
    allowed_mentions: Optional[Any] = None,
    view: Optional[Union[View, Dict[str, Any]]] = None,
    attachments: Optional[List[Any]] = None,
    embed: Optional[Embed] = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {"content": content}
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

    if view:
        if isinstance(view, dict):
            payload.update({"components": view})
        else:
            payload.update({"components": view.to_dict()})
    else:
        payload.update({"components": None})
    return payload
