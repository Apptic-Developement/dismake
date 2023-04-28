from __future__ import annotations
from typing import List, Optional, TYPE_CHECKING

from pydantic import BaseModel
from ..models import Interaction
from .select_option import SelectOption
from ..errors import InteractionResponded
from ..params import handle_edit_params
from ..enums import InteractionResponseType
if TYPE_CHECKING:
    from .house import House
class MessageComponentData(BaseModel):
    custom_id: str
    component_type: int
    values: Optional[List[SelectOption]]


class ModalSubmitData(BaseModel):
    custom_id: str
    # components	array of message components	the values submitted by the user


class ComponentContext(Interaction):
    data: Optional[MessageComponentData]

    async def edit_message(
        self, content: str, *, tts: bool = False, house: Optional[House] = None
    ):
        if self.is_responded:
            raise InteractionResponded(self)
        if house:
            self.bot.add_house(house)
        payload = handle_edit_params(content=content, tts=tts, house=house)
        return await self.bot._http.client.request(
            method="POST",
            url=f"/interactions/{self.id}/{self.token}/callback",
            json={
                "type": InteractionResponseType.UPDATE_MESSAGE.value,
                "data": payload,
            },
        )


class ModalContext(Interaction):
    data: Optional[ModalSubmitData]
