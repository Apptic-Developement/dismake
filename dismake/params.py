from __future__ import annotations
from typing import Any, Optional
from .enums import MessageFlags

def handle_send_params(
    content: str,
    *,
    tts: Optional[bool] = None,
    embeds: Optional[list] = None,
    allowed_mentions: Optional[Any] = None,
    components: Optional[list[Any]] = None,
    attachments: Optional[list[Any]] = None,
    embed: Optional[Any] = None,
    ephemeral: bool = False,
):
    payload: dict[str, Any] = {"content": content}
    if ephemeral:
        payload.update({"flags": MessageFlags.EPHEMERAL.value})
    if tts:
        payload.update({"tts": tts})
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



