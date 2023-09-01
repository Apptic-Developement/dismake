from dismake import Embed
from discord import Embed as DEmbed
from pprint import pprint as print

demb = DEmbed(title="Okk", description="Hmm").set_author(name="Okk")

embed = Embed(title="Test Title", description="Test Description")

print(Embed.from_dict({'author': {'name': 'Okk'},
 'description': 'Hmm',
 'title': 'Okk',
 'type': 'rich'}).to_dict())