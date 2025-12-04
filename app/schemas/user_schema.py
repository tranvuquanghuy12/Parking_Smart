from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    phone: str
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    phone: str
