from pydantic import BaseModel
from datetime import datetime

class MessageCreateReqBody(BaseModel):
    chat_id: int
    text: str

class MessageSchema(BaseModel):
    id: int
    chat_id: int
    sender_id: int
    text: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }