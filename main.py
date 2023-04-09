import dismake, config
from dismake import SlashCommand, Option, Context
from dismake import Choice
from dismake.enums import OptionType


app = dismake.Bot(
    token=config.token,
    client_public_key=config.public_key,
    client_id=config.client_id,
    route="/",
)


@app.event("ready")
async def on_ready():
    print("Logged in as %s" % app.user)
    # await app.sync_commands()


class Autocomplete(SlashCommand):
    def __init__(self):
        super().__init__(
            name="autocomplete",
            description="Testing autocomplete.",
            options=[
                Option(
                    name="buy",
                    description="Buy products.",
                    type=OptionType.SUB_COMMAND_GROUP,
                    options=[
                        Option(
                            name="fruit",
                            description="Buy a fruit.",
                            type=OptionType.SUB_COMMAND,
                            options=[
                                Option(
                                    name="name", description="Your name?", required=True
                                ),
                                Option(
                                    name="fav-fruit",
                                    description="Fruits with your name.",
                                    autocomplete=True,
                                    required=True,
                                ),
                                Option(
                                    name="quantity",
                                    description="How many fruit(s) you want.",
                                    autocomplete=True,
                                    required=True,
                                ),
                            ],
                        )
                    ],
                )
            ],
        )

    async def callback(self, ctx: Context):
        f = ctx.get_focused
        await ctx.respond(
            f"You got: {ctx.namespace.fav_fruit}\nQuantity: {ctx.namespace.quantity}\nThanks for shoping {ctx.namespace.name}!"
        )

    async def autocomplete(self, ctx: Context):
        fruit_command = ctx.subcommands.fruit
        if fruit_command:
            focused = ctx.get_focused
            assert focused is not None
            if focused.name == "fav-fruit":
                fruits = ["Apple", "Banana", "Mango"]
                return [
                    Choice(name=f"{ctx.namespace.name} {fruit}", value=fruit)
                    for fruit in fruits
                ]
            elif focused.name == "quantity":
                quantitys = [
                    "One",
                    "Two",
                    "Three",
                ]
                return [Choice(name=name) for name in quantitys]


app.add_commands([Autocomplete()])


if __name__ == "__main__":
    app.run(app=f"main:app", reload=True)
