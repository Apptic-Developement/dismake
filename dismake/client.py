from __future__ import annotations

from typing import TYPE_CHECKING, Sequence, Any, Optional, Type
from .http import HttpClient
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
from logging import getLogger
from .models import Interaction

if TYPE_CHECKING:
    from typing_extensions import Self
log = getLogger(__name__)


__all__: Sequence[str] = ("Client",)


class Client:
    def __init__(
        self,
        token: str,
        application_id: int,
        public_key: str,
        *,
        interaction_cls: Type[Interaction[Self]] = Interaction,
    ) -> None:
        self.http: HttpClient = HttpClient(token=token, application_id=application_id)
        self._verify_key = VerifyKey(key=bytes.fromhex(public_key))
        self._interaction_cls = interaction_cls

    def verify(self, signature: str, timestamp: str, body: bytes) -> Optional[bool]:
        try:
            self._verify_key.verify(
                smessage=timestamp.encode() + body, signature=bytes.fromhex(signature)
            )
        except BadSignatureError:
            return False
        else:
            return True

    async def parse_interactions(self, body: dict[str, Any]) -> Any:
        ...
