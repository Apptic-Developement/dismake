from discord import Permissions
from dismake import flags

print(Permissions(kick_members=True, ban_members=True))
print((flags.Permissions.KICK_MEMBERS | flags.Permissions.BAN_MEMBERS).value)