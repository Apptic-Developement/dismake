from __future__ import annotations

from typing import Optional, List, TYPE_CHECKING

from ..interaction import Interaction, ApplicationCommandData, ApplicationCommandOption
from ..enums import InteractionResponseType, MessageFlags, OptionType
from ..params import handle_send_params

if TYPE_CHECKING:
    from .command import SlashCommand

__all__ = ("Context",)


class Context(Interaction):
    data: Optional[ApplicationCommandData]

    async def respond(
        self, content: str, *, tts: bool = False, ephemeral: bool = False
    ):
        await self.request.app._http.client.request(
            method="POST",
            url=f"/interactions/{self.id}/{self.token}/callback",
            json={
                "type": InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE.value,
                "data": handle_send_params(
                    content=content, tts=tts, ephemeral=ephemeral
                ),
            },
            headers=self.request.app._http.headers,
        )

    async def defer(self, thinking: bool = True):
        await self.request.app._http.client.request(
            method="POST",
            url=f"/interactions/{self.id}/{self.token}/callback",
            json={
                "type": InteractionResponseType.DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE.value,
                "data": {"flags": MessageFlags.LOADING.value} if not thinking else None,
            },
            headers=self.request.app._http.headers,
        )

    async def send_followup(
        self, content: str, *, tts: bool = False, ephemeral: bool = False
    ):
        return await self.request.app._http.client.request(
            method="POST",
            url=f"/webhooks/{self.application_id}/{self.token}",
            json=handle_send_params(content=content, tts=tts, ephemeral=ephemeral),
            headers=self.request.app._http.headers,
        )

    @property
    def command(self) -> Optional[SlashCommand]:
        assert self.data is not None
        return self.bot.get_command(self.data.name)

    @property
    def namespace(self) -> Namespace:
        kwargs = {}
        if (data := self.data) is None or (options := data.options) is None:
            return Namespace()

        opts: Optional[List[ApplicationCommandOption]] = list()
        for option in options:
            if o_opts := option.options:
                for o_opt in o_opts:
                    opts.append(o_opt)

            opts.append(option)
        if not opts:
            return Namespace()
        for opt in opts:
            if opt.type in (OptionType.SUB_COMMAND, OptionType.SUB_COMMAND_GROUP):
                kwargs[opt.name.replace("-", "_")] = True
            else:
                kwargs[opt.name.replace("-", "_")] = opt.value
        return Namespace(**kwargs)


class Namespace:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            self.__dict__[k] = v

    def __getattr__(self, attr: str):
        return None
