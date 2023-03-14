import dismake, config
from dismake.app_commands import SlashCommand, Option, Choice

app = dismake.Bot(
    token=config.token, client_public_key=config.public_key, client_id=config.client_id
)

s = SlashCommand(
    name="sdfbb",
    description="Okiee",
    options=[
        Option(
            name="o1",
            description="Option 1's description",
            choices=[
                Choice(name="ok", value="Okiee"),
                Choice(name="ok2", value="Okie2"),
                Choice(name="o3", value="Okiee3"),
            ],
        ),
        Option(name="o2", description="Option 2's description"),
        Option(name="o3", description="Option 3's description", required=True),
    ],
)
print(s.dict(exclude_none=True))


# if __name__ == "__main__":
#     app.run(app=f"main:app", reload=True)
