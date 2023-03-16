import dismake, config

app = dismake.Bot(
    token=config.token, client_public_key=config.public_key, client_id=config.client_id
)

@app.on_event("startup")
async def on_startup():
    print(await app.sync_commands())

@app.command(
    name="command",
    description="Command description",
    options=[
        dismake.Option(name="option1", description="Option 1 description"),
        dismake.Option(name="option2", description="Option 2 description"),
        dismake.Option(
            name="choice",
            description="Choice description",
            choices=[dismake.Choice(name="choice1"), dismake.Choice(name="choice2")],
        ),
    ],
)
async def command(interaction):
    pass


@command.sub_command(
    "sub_command",
    "subcommand description",
)
async def subcommand(interaction):
    pass


@subcommand.command(
    "onemore",
    "oooo",
    options=[
        dismake.Option(name="option1", description="Option 1 description"),
        dismake.Option(name="option2", description="Option 2 description"),
        dismake.Option(
            name="choice",
            description="Choice description",
            choices=[dismake.Choice(name="choice1"), dismake.Choice(name="choice2")],
        ),
    ],
)
async def more(interaction):
    pass



if __name__ == "__main__":
    app.run(app=f"main:app", reload=True)
