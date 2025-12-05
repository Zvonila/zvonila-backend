from pydantic import BaseModel, EmailStr

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserRegister(BaseModel):
    email: EmailStr
    name: str
    password: str

class TokenSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserSchema(BaseModel):
    id: int
    name: str
    email: EmailStr
    avatar_url: str | None

    model_config = {
        "from_attributes": True
    }