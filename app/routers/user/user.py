
from fastapi import Response, status, HTTPException, Depends , APIRouter
from sqlalchemy.orm import Session
from ... import   utlis
from ..auth import oauth2
from . import user_crud as crud, user_schemas
from app.database import  get_db


router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=user_schemas.User)
async def creat_user(user: user_schemas.UserCreate, db: Session = Depends(dependency=get_db)):
    password_hash = utlis.get_password_hash(user.password)
    user.password = password_hash
    return crud.create_user(db, user)


@router.get("/{id}", response_model=user_schemas.User)
async def get_user(id: int, response: Response, db: Session = Depends(dependency=get_db), user_id: int = Depends(oauth2.get_current_user)):
    user = crud.get_user(db, id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"User with id {id} not found",
            )
    return user