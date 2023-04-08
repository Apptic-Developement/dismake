import dismake, config
from dismake.builders import SlashCommandBuilder, Option, Choice
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


class Echo(SlashCommandBuilder):
    def __init__(self):
        super().__init__(
            "echo",
            "Echo something!",
            options=[
                Option(name="text", description="Say something...", required=True),
                Option(
                    name="fav-fruits",
                    description="Tell me what is your fav fruit...",
                    required=True,
                    choices=[
                        Choice(name="apple"),
                        Choice(name="mango"),
                        Choice(name="banana"),
                    ],
                ),
                Option(
                    name="response-type",
                    description="Choose a response type",
                    required=True,
                    type=OptionType.BOOLEAN,
                ),
            ],
        )

    async def callback(self, interaction: dismake.CommandInteraction):
        assert interaction.data is not None
        return print(interaction.data.options[1].value)


app.add_commands([Echo()])
print(Echo().to_dict())
if __name__ == "__main__":
    app.run(app=f"main:app", reload=True)
