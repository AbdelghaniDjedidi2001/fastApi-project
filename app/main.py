from random import randrange
from typing import Optional
from fastapi import FastAPI , Response, status, HTTPException
from pydantic import BaseModel


app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_postes = [{"id":1,"title":"title1","content":"this is the content of post 1"}]

def find_index_post(id):
    for index, post in enumerate(my_postes):
        if post["id"] == id:
            return index
def find_post(id):
    for post in my_postes:
        if post["id"] == id:
            return post


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/posts")
async def get_posts():
    return {"data": my_postes}

@app.get("/posts/{id}")
async def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with id {id} not found",
            )
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"detail": f"Post with id {id} not found"}
    return {"data": post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def creat_post(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0,1000000)
    my_postes.append(post_dict)
    return {"data": post_dict}



@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with id {id} not found",
            )
    my_postes.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@app.put("/posts/{id}")
async def update_post(id: int, post: Post):
    post_dict = post.model_dump()
    index = find_index_post(id)
    if index == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with id {id} not found",
            )
    post_dict['id'] = id
    my_postes[index] = post_dict
    return {"data": post_dict}