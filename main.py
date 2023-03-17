import dismake, config

app = dismake.Bot(
    token=config.token, client_public_key=config.public_key, client_id=config.client_id
)


@app.command(name="rolemenu", description="Rolemenu command")
async def rolemenu(interaction):
    pass


@app.on_event("startup")
async def on_startup():
    # print(await app.sync_commands())
    pass


@rolemenu.sub_command(name="create", description="Rolemenu create command")
async def create(interaction):
    pass


@rolemenu.sub_command(name="edit", description="Rolemenu edit")
async def edit(interaction):
    pass


@edit.sub_command(name="button", description="Edit a button")
async def button(interaction):
    pass


@edit.sub_command(name="dropdown", description="Edit a dropdown")
async def dropdown(interaction):
    pass


@edit.sub_command(name="placeholder", description="Edit a placeholder")
async def placeholder(interaction):
    pass


@rolemenu.sub_command(name="delete", description="Delete something")
async def delete(interaction):
    pass


@delete.sub_command(name="button", description="Delete a button")
async def dbutton(interaction):
    pass


@delete.sub_command(name="dropdown", description="Delete a dropdown")
async def ddropdown(interaction):
    pass


if __name__ == "__main__":
    app.run(app=f"main:app", reload=True)

