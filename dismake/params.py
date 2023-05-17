from __future__ import annotations
from typing import Any, Dict, List, Optional, TYPE_CHECKING, Union

from .enums import MessageFlags

if TYPE_CHECKING:
    from .ui import View


__all__ = ("handle_send_params", "handle_edit_params")


def handle_send_params(
    content: str,
    *,
    tts: Optional[bool] = None,
    embeds: Optional[list] = None,
    allowed_mentions: Optional[Any] = None,
    view: Optional[Union[View, Dict[Any, Any]]] = None,
    attachments: Optional[List[Any]] = None,
    embed: Optional[Any] = None,
    ephemeral: bool = False,
):
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
    _embeds = list()
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
    embeds: Optional[list] = None,
    allowed_mentions: Optional[Any] = None,
    view: Optional[Union[View, Dict[str, Any]]] = None,
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

    if view:
        if isinstance(view, dict):
            payload.update({"components": view})
        else:
            payload.update({"components": view.to_dict()})
    else:
        payload.update({"components": None})
    return payload
