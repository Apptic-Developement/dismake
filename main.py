import dismake, config

app = dismake.Bot(
    token=config.token, client_public_key=config.public_key, client_id=config.client_id
)


@app.command(
    name="hello",
    description="Prompt your's name.",
    options=[
        dismake.Option(
            name="name",
            description="Enter your name",
            choices=[dismake.Choice(name="Okiee")],
        )
    ],
)
async def hmm(interaction):
    pass





print(hmm.payload)
if __name__ == "__main__":
    app.run(app=f"main:app", reload=True)

