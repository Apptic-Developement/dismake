import dismake, config, logging
from commands import get_commands


app = dismake.Bot(
    token=config.token,
    client_public_key=config.public_key,
    client_id=config.client_id,
    route="/",
)


@app.event("ready")
async def on_ready():
    print("Logged in as %s" % app.user)
    sync = await app.sync_commands()
    print(sync.text)



app.add_commands(get_commands(app))
if __name__ == "__main__":
    app.run(app=f"main:app", reload=True)
