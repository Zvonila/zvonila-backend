from pydantic import BaseModel

class CallOfferSchema(BaseModel):
    sdp: str
    type: str

class CallCreateSchema(BaseModel):
    offer: CallOfferSchema