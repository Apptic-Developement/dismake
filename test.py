# from discord import app_commands

# c = app_commands.Group(name="slash", description="Hmm...")
# c2 = app_commands.Group(name="sub_group", description="Hmm...2", parent=c)
# a = {
#     "name": "slash",
#     "description": "Hmm...",
#     "type": 1,
#     "options": [
#         {"name": "sub_group", "description": "Hmm...2", "type": 2, "options": []}
#     ],
#     "nsfw": False,
#     "dm_permission": True,
#     "default_member_permissions": None,
# }
# print(c.to_dict())

from dismake import app_commands, Permissions

c = app_commands.Group(
    name="slash",
    description="Hmm...",
    guild_only=True,
    default_member_permissions=Permissions(manage_guild=True),
)
c2 = app_commands.Group(name="sub_group", description="Hmm...2", parent=c)

print(c.to_dict())
