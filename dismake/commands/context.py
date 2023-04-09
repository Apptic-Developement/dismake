from __future__ import annotations

from typing import Optional, List, TYPE_CHECKING

from ..interaction import Interaction, ApplicationCommandData, ApplicationCommandOption
from ..enums import InteractionResponseType, InteractionType, MessageFlags, OptionType
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
    def is_autocomplete(self) -> bool:
        return self.type == InteractionType.APPLICATION_COMMAND_AUTOCOMPLETE.value

    @property
    def get_options(self) -> Optional[List[ApplicationCommandOption]]:
        if (data := self.data) is None or (options := data.options) is None:
            return None

        opts = list()
        for option in options:
            if option.type == OptionType.SUB_COMMAND and option.options:
                for command in option.options:
                    opts.append(command)
            elif option.type == OptionType.SUB_COMMAND_GROUP and (
                sub_commands := option.options
            ):
                for sub_command in sub_commands:
                    if sub_command_options := sub_command.options:
                        for sub_command_option in sub_command_options:
                            opts.append(sub_command_option)
            else:
                opts.append(option)
        return opts

    @property
    def get_focused(self):
        if not self.is_autocomplete:
            raise TypeError(f"Only autocomplete interactions have focused values.")

        if not (opts := self.get_options):
            return None
        filtered_opts = list(filter(lambda option: option.focused == True, opts))
        if filtered_opts:
            return filtered_opts[0]

    @property
    def subcommands(self) -> Subcommands:
        if (data := self.data) is None or (options := data.options) is None:
            return Subcommands()

        s_commands: Optional[List[ApplicationCommandOption]] = list()
        for option in options:
            if option.type == OptionType.SUB_COMMAND_GROUP and (
                commands := option.options
            ):
                for command in commands:
                    s_commands.append(command)
            elif option.type == OptionType.SUB_COMMAND:
                s_commands.append(option)
        kwargs = {}
        for command in s_commands:
            kwargs[command.name] = True

        return Subcommands(**kwargs)

    @property
    def namespace(self) -> Namespace:
        kwargs = {}
        if (options := self.get_options) is None:
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


class Subcommands:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            self.__dict__[k] = v

    def __getattr__(self, attr: str):
        return None
