from typing import Optional, Annotated
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


@app.command("choose", "This is a sub command 1.")
async def sub_command1(
    ctx, 
    name: Annotated[str, app_commands.Option("name", "What is your name?", required=True)],
    age: Annotated[int, app_commands.Option("age", "What is your age?", required=True, type=int)]
):
    
    await ctx.send(f"Your name is: {name} and agee is: {age}?")




if __name__ == "__main__":
    app.run(app=f"main:app", reload=True)
