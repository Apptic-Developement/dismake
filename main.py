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
                    name="fruit",
                    description="Create a new rolemenu.",
                    type=OptionType.SUB_COMMAND,
                    options=[
                        Option(name="your-name", description="Your name?"),
                        Option(
                            name="fav-fruit",
                            description="Fruits with your name.",
                            autocomplete=True,
                        ),
                    ],
                )
            ],
        )

    async def callback(self, interaction: Context):
        await interaction.respond(
            f"Okay! So your favourite fruit is {interaction.namespace.fav_fruit}"
        )

    async def autocomplete(self, interaction: Context):
        fruits = ["Apple", "Banana", "Mango"]
        return [
            Choice(name=f"{interaction.namespace.your_name} {fruit}", value=fruit)
            for fruit in fruits
        ]


app.add_commands([Autocomplete()])


if __name__ == "__main__":
    app.run(app=f"main:app", reload=True)
