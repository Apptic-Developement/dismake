import dismake, config

app = dismake.Bot(
    token=config.token, client_public_key=config.public_key, client_id=config.client_id
)

@app.command(
    name="haha",
    description="Okee"
)
async def hmm(interaction):
    pass

print(app._global_application_commands)
print(app._guild_application_commands)
print(hmm.payload)


# if __name__ == "__main__":
#     app.run(app=f"main:app", reload=True)
