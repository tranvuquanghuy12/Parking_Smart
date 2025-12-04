from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    id: Optional[str] = None
    email: str
    phone: str
    password: str
