from fastapi import FastAPI, Request , Response, status, HTTPException, Depends 
from typing import List
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import engine , get_db

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}



@app.get("/posts", response_model=List[schemas.Post])
async def get_posts(db: Session = Depends(dependency=get_db)):
    posts = crud.get_posts(db) 
    return posts
    



@app.get("/posts/{id}", response_model=schemas.Post)
async def get_post(id: int, response: Response, db: Session = Depends(dependency=get_db)):
    post = crud.get_post(db, id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with id {id} not found",
            )
    return post



@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def creat_post(post: schemas.PostCreate, db: Session = Depends(dependency=get_db)):
    post = crud.create_post(db, post)
    return post



@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(dependency=get_db)):
    post = crud.delete_post(db, id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with id {id} not found",
            )
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Post)
async def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(dependency=get_db)):
    post = crud.update_post(db, id, post)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with id {id} not found",
            )
    return post

