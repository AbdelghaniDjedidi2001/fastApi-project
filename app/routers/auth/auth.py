from fastapi import FastAPI, Depends, HTTPException, status, Response, APIRouter, Request
from sqlalchemy.orm import Session
from ... import models
from ...database import get_db
from . import auth_crud as crud, oauth2
from ...utlis import get_password_hash, verify_password
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from . import auth_schemas

router = APIRouter(
    prefix= "/auth",
    tags=["authentications"],
)


@router.post("/login")
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, user_credentials.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    if not verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    access_token = oauth2.create_access_token(data={"sub": user.id})
    return {"access_token": access_token, "token_type": "bearer"}