from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    published: Optional[bool] = None
    
class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    craeted_at: datetime
    class Config:
        from_attributes = True
        
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
