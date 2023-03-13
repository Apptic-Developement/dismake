import dismake, config
from dismake.command import Option
from dismake import Interaction
from dismake import OptionType

app = dismake.Bot(
    token=config.token, client_public_key=config.public_key, client_id=config.client_id
)


@app.on_event("startup")
async def on_startup():
    # print(await app.sync_commands())
    # print(app.user.display_avatar)
    print(app.user.username)
    


options = [
    Option(name="name", description="Enter your name", type=OptionType.STRING.value),
    Option(name="age", description="Enter your age", type=OptionType.INTEGER.value),
]

@app.command(name="ping", description="Ping Command", options=options)
async def ping(interaction: Interaction):
    await interaction.respond("Responded! Dismake :)", ephemeral=True)

