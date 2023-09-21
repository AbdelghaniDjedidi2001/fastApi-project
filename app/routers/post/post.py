
from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session
from . import  post_schemas
from . import post_crud as crud
from app.database import  get_db


router = APIRouter(
    prefix="/posts",
    tags=["posts"],
)


@router.get("/", response_model=List[post_schemas.Post])
async def get_posts(db: Session = Depends(dependency=get_db)):
    posts = crud.get_posts(db) 
    return posts
    



@router.get("/{id}", response_model=post_schemas.Post)
async def get_post(id: int, response: Response, db: Session = Depends(dependency=get_db)):
    post = crud.get_post(db, id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with id {id} not found",
            )
    return post



@router.post("/", status_code=status.HTTP_201_CREATED, response_model=post_schemas.Post)
async def creat_post(post: post_schemas.PostCreate, db: Session = Depends(dependency=get_db)):
    post = crud.create_post(db, post)
    return post



@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(dependency=get_db)):
    post = crud.delete_post(db, id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with id {id} not found",
            )
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=post_schemas.Post)
async def update_post(id: int, post: post_schemas.PostCreate, db: Session = Depends(dependency=get_db)):
    post = crud.update_post(db, id, post)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with id {id} not found",
            )
    return post
