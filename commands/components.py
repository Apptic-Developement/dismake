from dismake import SlashCommand, Context, Bot, Option, OptionType, ComponentContext
from dismake import ui


class House(ui.House):
    def __init__(self) -> None:
        super().__init__()
        self.count: int = 0


house = House()


@house.button(label="Click", custom_id="random_number_gusser")
async def click_me(ctx: ComponentContext):
    house.count += 1
    view.label = str(house.count)
    await ctx.edit_message(f"Click to increase count.", house=house)


@house.button(label=f"0", disabled=True)
async def view(ctx: ComponentContext):
    ...


class Component(SlashCommand):
    def __init__(self, bot: Bot):
        super().__init__(
            name="components",
            description="Testing components.",
            options=[
                Option(
                    name="button",
                    description="Test button.",
                    type=OptionType.SUB_COMMAND,
                )
            ],
        )

    async def callback(self, ctx: Context):
        if ctx.namespace.button:
            await ctx.respond(f"Button", house=house)
