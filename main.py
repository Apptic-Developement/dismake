import dismake, config
from dismake.builders import SlashCommandBuilder, Option
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


class RoleMenu(SlashCommandBuilder):
    def __init__(self):
        super().__init__(
            name="rolemenu",
            description="Create awesome rolemenus.",
            options=[
                Option(
                    name="create",
                    description="Create a new rolemenu.",
                    type=OptionType.SUB_COMMAND,
                    options=[Option(name="name", description="Name of the rolemenu.")],
                )
            ],
        )

    async def callback(self, interaction: dismake.CommandInteraction):
        ...


app.add_commands([RoleMenu()])


if __name__ == "__main__":
    app.run(app=f"main:app", reload=True)
