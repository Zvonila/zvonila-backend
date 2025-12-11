from typing import Literal
from pydantic import BaseModel
from .models import CallStatus, CallType, ParticipantRole, ParticipantStatus
from typing import Optional
from datetime import datetime

class CallCreateSchema(BaseModel):
    offer: str
    to_user_id: int
    type: CallType

class CallCancelSchema(BaseModel):
    call_id: int

class CallAcceptSchema(BaseModel):
    answer: str
    call_id: int

class CallDeclineSchema(BaseModel):
    call_id: int

class CallEndSchema(BaseModel):
    call_id: int

class ParticipantSchema(BaseModel):
    id: int
    call_id: int
    user_id: int
    role: ParticipantRole
    status: ParticipantStatus
    joined_at: Optional[datetime]
    left_at: Optional[datetime]

    class Config:
        from_attributes = True

class CallSchema(BaseModel):
    id: int
    initiator_id: int
    type: CallType
    status: CallStatus

    created_at: datetime
    answered_at: Optional[datetime]
    ended_at: Optional[datetime]
    last_update_at: Optional[datetime]

    class Config:
        from_attributes = True