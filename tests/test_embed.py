from dismake import Embed
from discord import Embed as DEmbed
import datetime, sys



embed = (Embed(title="Test Title",description="Test Description",url="https://google.com/",timestamp=datetime.datetime.utcnow())
    .set_author(name="Ok")
    .set_footer(text="OkFooter")
    .add_field(name="Field 1", value="Field Value 1")
    .add_field(name="Field 2", value="Field Value 2")
    .add_field(name="Field 3", value="Field Value 3"))

print(embed.to_dict())
print("Discord Embed Size: ", sys.getsizeof(DEmbed.from_dict(embed.to_dict())))
print("Dismake Embed Size: ", sys.getsizeof(Embed.from_dict(embed.to_dict())))