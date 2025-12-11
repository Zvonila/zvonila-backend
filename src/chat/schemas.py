from typing import Optional
from pydantic import BaseModel
from datetime import datetime

from src.auth.schemas import UserSchema
from src.message.schemas import MessageSchema

class ChatSchema(BaseModel):
    id: int
    username: str
    initiator_id: int
    receiver_id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }

class ChatWithDetails(ChatSchema):
    companion: UserSchema
    last_message: Optional[MessageSchema] = None

class CreateChatReqBody(BaseModel):
    receiver_id: int