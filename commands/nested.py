import dismake
from dismake.enums import OptionType


class NestedCommand(dismake.SlashCommand):
    def __init__(self, bot: dismake.Bot):
        super().__init__(
            name="level_1",
            description="This is level 1.",
            options=[
                dismake.Option(
                    name="level_2",
                    description="This is level 2.",
                    type=dismake.OptionType.SUB_COMMAND_GROUP,
                    options=[
                        dismake.Option(
                            name="level_3",
                            description="This is level 3.",
                            type=dismake.OptionType.SUB_COMMAND,
                        ),
                    ],
                ),
                dismake.Option(
                    name="groups",
                    description="This is a command group.",
                    type=dismake.OptionType.SUB_COMMAND_GROUP,
                    options=[
                        dismake.Option(
                            name="string",
                            description="This is a string option.",
                            type=OptionType.SUB_COMMAND,
                        )
                    ],
                ),
            ],
        )
        self.bot = bot

    async def callback(self, ctx: dismake.Context):
        return await super().callback(ctx)
