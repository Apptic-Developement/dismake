import dismake, config
from commands import get_commands

app = dismake.Bot(
    token=config.token,
    client_public_key=config.public_key,
    client_id=config.client_id,
    route="/",
)


@app.event(dismake.Events.Ready)
async def on_ready():
    print("Logged in as %s" % app.user)
    await app.sync_commands()


# @app.event(dismake.Events.InteractionCreate)
# async def interaction_create(interaction: dismake.Interaction, payload: dict):
#     print(payload)


app.add_commands(get_commands(app))


if __name__ == "__main__":
    app.run(app=f"main:app", reload=True)

c = {
    "type": 1,
    "components": [
        {
            "style": 3,
            "label": "yes",
            "custom_id": "8e546091-07a1-4f1b-9099-ff661c49087f",
            "disabled": False,
            "type": 2,
        },
        {
            "style": 4,
            "label": "no",
            "custom_id": "8569e61e-4ee7-4e91-83bf-5037df31bfe9",
            "disabled": False,
            "type": 2,
        },
    ],
}
