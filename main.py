import dismake, config

app = dismake.Bot(
    token=config.token, client_public_key=config.public_key, client_id=config.client_id
)


@app.on_event("startup")
async def on_startup():
    print("Ok")
    # if gc := app.get_commands():
    #     for command in gc:
    #         await app._http.register_command(command)
    # await app._http.get_global_commands(only_names=True)
    print(await app._http.remove_all_commands())


@app.command(name="ping", description="Ping Command")
async def ping_cb(interaction):
    pass


# make = [
#     {
#         "id": "1083693896900550727",
#         "application_id": "1071851326234951770",
#         "dm_permission": False,
#         "version": "1083693896900550728",
#         "options": [
#             {"name": "start", "description": "Starts a new giveaway.", "type": 1},
#             {"name": "reroll", "description": "Reroll a giveaway.", "type": 1},
#         ],
#         "default_permission": True,
#         "nsfw": False,
#         "default_member_permissions": "8192",
#         "type": 1,
#         "name": "giveaway",
#         "description": "Create awesome giveaways with apptic bot.",
#     },
#     {
#         "id": "1083695286955823105",
#         "application_id": "1071851326234951770",
#         "dm_permission": True,
#         "version": "1083760907118714900",
#         "default_permission": True,
#         "nsfw": False,
#         "default_member_permissions": None,
#         "type": 1,
#         "name": "test",
#         "description": "This is test command",
#     },
#     {
#         "id": "1083962321224863865",
#         "application_id": "1071851326234951770",
#         "dm_permission": True,
#         "version": "1083962321224863866",
#         "default_permission": True,
#         "nsfw": False,
#         "default_member_permissions": None,
#         "type": 1,
#         "name": "ping",
#         "description": "Ping Command",
#     },
# ]
