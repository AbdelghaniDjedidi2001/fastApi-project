from fastapi import  Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session

from . import oauth2
from ...database import get_db
from . import auth_crud as crud, auth_schemas
from ...utlis import  verify_password
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(
    prefix= "/auth",
    tags=["authentications"],
)


@router.post("/login",response_model=auth_schemas.Token)
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, user_credentials.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials",
        )
    if not verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials",
        )
    access_token = oauth2.create_access_token(data={"sub": str(user.id)},)
    return {"access_token": access_token, "token_type": "bearer"}