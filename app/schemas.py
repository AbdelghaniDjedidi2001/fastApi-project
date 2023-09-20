from typing import Optional
from pydantic import BaseModel
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
        orm_mode = True
