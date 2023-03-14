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
    Option(name="name", description="Enter your name", type=OptionType.STRING.value, required=True),
]

@app.command(name="hello", description="I will echo your name.", options=options)
async def ping(interaction: Interaction):
    await interaction.respond(f"Hello {interaction.data.options[0].value}!")
    





if __name__ == "__main__":
    app.run(app=f"main:app", reload=True)

