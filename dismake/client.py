from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, Dict, Optional, Sequence, Type, Union
from functools import wraps
from logging import getLogger

from nacl.exceptions import BadSignatureError
from nacl.signing import VerifyKey

from .commands import Command, Group
from .http import HttpClient
from .models import Interaction

if TYPE_CHECKING:
    from typing_extensions import Self

    from .enums import Locale
    from .models import Permissions
    from .types import AsyncFunction, InteractionData


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

    Attributes
    ----------
    http: HttpClient
        The HTTP client that will be used to make requests to Discord.
    """

    def __init__(
        self,
        token: str,
        application_id: str,
        public_key: str,
    ) -> None:
        self.http: HttpClient = HttpClient(token=token, application_id=application_id)
        self._verify_key = VerifyKey(key=bytes.fromhex(public_key))
        self._application_commands: Dict[str, Union[Command[Self], Group[Self]]] = {}

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
        interaction = Interaction(client=self, data=data)

        if interaction.is_application_command:
            ...
        if interaction.is_message_component:
            ...
        if interaction.is_modal_submit:
            ...

    def command(
        self,
        name: str,
        description: str,
        name_localizations: Optional[Dict[Locale, str]] = None,
        description_localizations: Optional[Dict[Locale, str]] = None,
        default_member_permissions: Optional[Permissions] = None,
        guild_only: Optional[bool] = None,
        guild_id: Optional[int] = None,
        nsfw: Optional[bool] = None,
        cls: Type[Command[Self]] = Command,
    ) -> Callable[[AsyncFunction], Command[Self]]:
        def decorator(func: AsyncFunction) -> Command[Self]:
            @wraps(func)
            def wrapper(*_: Any, **__: Any) -> Command[Self]:
                command = cls(
                    callback=func,
                    client=self,
                    name=name,
                    description=description,
                    name_localizations=name_localizations,
                    description_localizations=description_localizations,
                    default_member_permissions=default_member_permissions,
                    guild_only=guild_only,
                    guild_id=guild_id,
                    nsfw=nsfw,
                )

                return command

            return wrapper()

        return decorator
