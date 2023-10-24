
from fastapi import Response, status, Depends, APIRouter
from sqlalchemy.orm import Session
from ..auth import oauth2
from ... import schemas
from . import vote_crud as crud
from app.database import get_db


router = APIRouter(
    prefix="/vote",
    tags=["vote"],
)

@router.post("/")
async def create_vote(vote: schemas.VoteCreate, db: Session = Depends(dependency=get_db), cur_user: schemas.User = Depends(oauth2.get_current_user)):
    return crud.create_vote(db, vote, cur_user)
