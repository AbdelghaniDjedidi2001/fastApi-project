
from fastapi import Response, status, Depends, APIRouter
from typing import List
from ..auth import oauth2
from sqlalchemy.orm import Session
from ... import schemas
from . import post_crud as crud
from app.database import  get_db


router = APIRouter(
    prefix="/posts",
    tags=["posts"],
)


@router.get("/", response_model=List[schemas.PostOut])
async def get_posts(db: Session = Depends(dependency=get_db), cur_user: int = Depends(oauth2.get_current_user),
                    limit: int = 15, skip: int = 0, search: str = ""):
    return crud.get_posts(db, skip, limit, search) 
     
    


@router.get("/{id}", response_model=schemas.PostOut)
async def get_post(id: int, response: Response, db: Session = Depends(dependency=get_db), cur_user: schemas.User  = Depends(oauth2.get_current_user)):
    return crud.get_post(db, id)



@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def creat_post(post: schemas.PostCreate, db: Session = Depends(dependency=get_db), cur_user: schemas.User  = Depends(oauth2.get_current_user)):
    user_id = int(cur_user.id)
    return crud.create_post(db,user_id, post)



@router.delete("/{id}", status_code=status.HTTP_202_ACCEPTED)
async def delete_post(id: int, db: Session = Depends(dependency=get_db), cur_user: schemas.User  = Depends(oauth2.get_current_user)):
    user_id = int(cur_user.id)
    return crud.delete_post(db,user_id,id) 



@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Post)
async def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(dependency=get_db), cur_user: schemas.User  = Depends(oauth2.get_current_user)):
    # user_id = int(cur_user.id)
    return crud.update_post(db,id,cur_user.id, post)
     
