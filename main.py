import dismake, config

app = dismake.Bot(
    token=config.token, client_public_key=config.public_key, client_id=config.client_id
)


rolemenu = dismake.Group(name="rolemenu", description="Rolemenu command")
edit = dismake.Group(name="edit", description="Edit rolemenu components", parent=rolemenu)


@edit.command(name="button", description="edit a rolemenu button")
async def callback(interaction):
    pass


app.add_command(rolemenu)

for n, c in app._global_application_commands.items():
    print(c.payload)
if __name__ == "__main__":
    app.run(app=f"main:app", reload=True)



