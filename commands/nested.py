import dismake


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
                        # Options
                        dismake.Option(
                            name="level_1",
                            description="This is level 1 option.",
                            type=dismake.OptionType.SUB_COMMAND,
                        ),
                        dismake.Option(
                            name="level_2",
                            description="This is 2 option.",
                            type=dismake.OptionType.SUB_COMMAND,
                        ),
                        dismake.Option(
                            name="level_3",
                            description="This is 3 option.",
                            type=dismake.OptionType.SUB_COMMAND,
                        )
                    ],
                )
            ],
        )
        self.bot = bot

    async def callback(self, ctx: dismake.Context):
        return await super().callback(ctx)