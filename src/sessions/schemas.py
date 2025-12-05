from pydantic import BaseModel
from datetime import datetime

class SessionSchema(BaseModel):
    id: int
    user_id: int
    ip: str
    user_agent: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }

class DeleteSessionReqBody(BaseModel):
    id: int