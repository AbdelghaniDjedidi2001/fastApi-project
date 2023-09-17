from random import randrange
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_postes = [{"id":1,"title":"title1","content":"this is the content of post 1"}]

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/posts")
async def root():
    return {"data": my_postes}

@app.post("/posts")
async def creat_post(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0,1000000)
    my_postes.append(post_dict)
    return {"data": post_dict}