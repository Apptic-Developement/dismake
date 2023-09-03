from dismake import Embed
from pprint import pprint as print
import datetime

print(
    Embed(
        title="Test Title",
        description="Test Description",
        url="https://google.com/",
        timestamp=datetime.datetime.utcnow(),
    )
    .set_author(name="Ok")
    .set_footer(text="OkFooter")
    .add_field(name="Field 1", value="Field Value 1")
    .add_field(name="Field 2", value="Field Value 2")
    .add_field(name="Field 3", value="Field Value 3")
    .to_dict()
)
