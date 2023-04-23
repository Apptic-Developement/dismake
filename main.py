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

d = [
    {
        "type": 1,
        "components": [
            {
                "type": 2,
                "style": 2,
                "disabled": False,
                "label": "Ok1",
                "custom_id": "21d29cfbc6be80b08dbd52bb8e2ea64c",
            },
            {
                "type": 2,
                "style": 2,
                "disabled": False,
                "label": "Ok2",
                "custom_id": "1f34b7a693a2453a77caff1e5989744e",
            },
            {
                "type": 2,
                "style": 2,
                "disabled": False,
                "label": "Ok3",
                "custom_id": "6c7ad2cad33acad47bd787980d300632",
            },
            {
                "type": 2,
                "style": 2,
                "disabled": False,
                "label": "Ok4",
                "custom_id": "2cfdc97b1d9a5062b46ef21cf81ce278",
            },
            {
                "type": 2,
                "style": 2,
                "disabled": False,
                "label": "Ok5",
                "custom_id": "37aff095c4024d39a8ef893b0d8067f9",
            },
        ],
    },
    {
        "type": 1,
        "components": [
            {
                "type": 2,
                "style": 2,
                "disabled": False,
                "label": "Ok6",
                "custom_id": "46795eb3b95c07b14c059dcc42de2628",
            },
            {
                "type": 2,
                "style": 2,
                "disabled": False,
                "label": "Ok7",
                "custom_id": "76842b47ffcf8b8ecfb3ae6336dfceef",
            },
            {
                "type": 2,
                "style": 2,
                "disabled": False,
                "label": "Ok8",
                "custom_id": "4cc0db65e59d4f80f67cd4116dae0da0",
            },
            {
                "type": 2,
                "style": 2,
                "disabled": False,
                "label": "Ok9",
                "custom_id": "eafb3a3e278bb0f8618b3cc22013ac37",
            },
            {
                "type": 2,
                "style": 2,
                "disabled": False,
                "label": "Ok10",
                "custom_id": "4fdc5d2500ab7365edb0532465b2de18",
            },
        ],
    },
]
