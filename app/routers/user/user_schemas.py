from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    pass
    password: str
    

 
class User(UserBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True
