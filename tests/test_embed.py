from dismake import Embed
from discord import Embed as DEmbed
from pprint import pprint as print

demb = DEmbed(title="Okk", description="Hmm").set_author(name="Okk").set_footer(text="Okk", icon_url="https://google.com/")

embed = Embed(title="Test Title", description="Test Description")

print(Embed.from_dict(demb.to_dict()).to_dict())

