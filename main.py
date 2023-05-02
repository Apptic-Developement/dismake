import dismake, config
from trees import group


from discord.ext import commands
commands.Bot.event

app = dismake.Bot(
    token=config.token,
    client_public_key=config.public_key,
    client_id=config.client_id,
    route="/",
)

group.tree.load(app)
@app.event("ready")
async def on_ready():
    print("Logged in as %s" % app.user)
    # sync = await app.sync_commands()
    # print(sync.text)

    




if __name__ == "__main__":
    app.run(app=f"main:app", reload=True)
