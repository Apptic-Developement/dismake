import dismake, config, logging
# from commands import get_commands

log = logging.getLogger(__name__)
app = dismake.Bot(
    token=config.token,
    client_public_key=config.public_key,
    client_id=config.client_id,
    route="/",
)


@app.event("ready")
async def on_ready():
    print("Logged in as %s" % app.user)
    await app.sync_commands()


@app.command("test", "This is a test command")
async def test_command(ctx: dismake.Context):
    await ctx.send("Ok?")

if __name__ == "__main__":
    app.run(app=f"main:app", reload=True)
