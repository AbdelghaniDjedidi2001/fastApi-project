from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, TypeVar


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


class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[str] = None


class PostBase(BaseModel):
    title: str
    content: str
    published: Optional[bool] = None
    
class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    craeted_at: datetime
    user_id: int
    user: User
    class Config:
        from_attributes = True

class PostOut(BaseModel):
    Post: Post
    votes: int
    class Config:
        from_attributes = True
    
class VoteBase(BaseModel):
    post_id: int
    value: int

class VoteCreate(VoteBase):
    pass

class Vote(VoteBase):
    pass
    user_id: int
    class Config:
        from_attributes = True