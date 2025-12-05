from pydantic import BaseModel
from datetime import datetime

class ChatSchema(BaseModel):
    id: int
    initiator_id: int
    receiver_id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }

class CreateChatReqBody(BaseModel):
    receiver_id: int