from typing import Optional
import dismake, config
from dismake import app_commands

# from commands import get_commands


app = dismake.Bot(
    token=config.token,
    client_public_key=config.public_key,
    client_id=config.client_id,
    route="/",
)


@app.event("ready")
async def on_ready():
    print("Logged in as %s" % app.user)
    # sync = await app.sync_commands()
    # print(sync.text)


group = app.create_group(name="slash", description="This is main command.")
sub_group = group.create_sub_group(
    name="sub_group", description="This is sub group command."
)

@group.command("sub_command1", "This is a sub command 1.", options=[
    app_commands.Option("name", "What is your name?")
])
async def sub_command1(ctx, name: str):
    await ctx.send(f"Your name is: {name} ?")


@sub_group.command("sub_command2", "This is a sub command 2.")
async def sub_command(ctx):
    await ctx.send("Sub command 2 bhi invoke ho gya re baba.")


if __name__ == "__main__":
    app.run(app=f"main:app", reload=True)
