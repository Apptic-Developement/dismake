from __future__ import annotations

from pydantic import BaseModel

class Role(BaseModel):
    id: int
    # Add more fields as needed

class ChannelMention(BaseModel):
    id: int
    # Add more fields as needed

class Attachment(BaseModel):
    # Define attachment fields
    pass

class Embed(BaseModel):
    # Define embed fields
    pass

class Reaction(BaseModel):
    # Define reaction fields
    pass

class MessageActivity(BaseModel):
    # Define message activity fields
    pass

class PartialApplication(BaseModel):
    # Define partial application fields
    pass

class MessageReference(BaseModel):
    # Define message reference fields
    pass
