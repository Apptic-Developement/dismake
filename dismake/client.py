from __future__ import annotations

from typing import Optional, Sequence, Any
from dismake.http import HttpClient
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

__all__: Sequence[str] = ("Client",)


class Client:
    def __init__(self, token: str, application_id: int, public_key: str) -> None:
        self.http: HttpClient = HttpClient(token=token, application_id=application_id)
        self._verify_key = VerifyKey(key=bytes.fromhex(public_key))

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
