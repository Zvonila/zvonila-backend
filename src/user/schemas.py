from pydantic import BaseModel

class ChangePasswordRequest(BaseModel):
    password: str
    new_password: str

class ChangeNameRequest(BaseModel):
    name: str
