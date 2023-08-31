from __future__ import annotations

from typing import TYPE_CHECKING, Sequence, Type
from logging import getLogger

from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

from .http import HttpClient
from .models import Interaction

if TYPE_CHECKING:
    from .types import InteractionData
    from typing_extensions import Self


log = getLogger(__name__)


__all__: Sequence[str] = ("Client",)


class Client:
    """Represents a client for interacting with the Discord API.

    Parameters
    -----------
    token: str
        The token of the bot.
    application_id: int
        The ID of the application that the bot is associated with.
    public_key: str
        The public key of the application.
    interaction_class: Type[Interaction[Self]]
        The class that will be used to represent interactions.

    Attributes
    ----------
    http: HttpClient
        The HTTP client that will be used to make requests to Discord.
    """

    def __init__(
        self,
        token: str,
        application_id: int,
        public_key: str,
        *,
        interaction_class: Type[Interaction[Self]],
    ) -> None:
        self.http: HttpClient = HttpClient(token=token, application_id=application_id)
        self._verify_key = VerifyKey(key=bytes.fromhex(public_key))
        self._interaction_class = interaction_class

    def create_interaction(self, data: InteractionData) -> Interaction[Self]:
        return self._interaction_class(client=self, data=data)

    def verify(self, signature: str, timestamp: str, body: bytes) -> bool:
        """Verify the incoming signature from Discord.

        Parameters
        ----------
        signature: str
            The signature from Discord.
        timestamp: str
            The timestamp from Discord.
        body: bytes
            The body of the request from Discord.

        Returns
        -------
        bool
            True if the signature is valid, False otherwise.
        """
        try:
            self._verify_key.verify(
                smessage=timestamp.encode() + body, signature=bytes.fromhex(signature)
            )
        except BadSignatureError:
            return False
        else:
            return True

    async def parse_interaction_create(self, data: InteractionData) -> None:
        """Parse and execute the appropriate action for an incoming interaction.

        Parameters
        ----------
        data: InteractionData
            The incoming interaction data.
        """
        interaction = self.create_interaction(data)
        
        if interaction.is_application_command:
            ...
        if interaction.is_message_component:
            ...
        if interaction.is_modal_submit:
            ...
