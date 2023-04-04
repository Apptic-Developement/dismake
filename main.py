import dismake, config
from dismake.builders import SlashCommandBuilder, Option, Choice



app = dismake.Bot(
    token=config.token,
    client_public_key=config.public_key,
    client_id=config.client_id,
    route="/",
)

@app.event('ready')
async def on_ready():
    print("Logged in as %s" % app.user)




if __name__ == "__main__":
    app.run(app=f"main:app", reload=True)
