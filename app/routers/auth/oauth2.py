from datetime import datetime, timedelta
from fastapi import Depends, HTTPException ,status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from . import auth_schemas
from . import auth_crud as crud
from ...database import SessionLocal, get_db

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def create_access_token(data: dict):
    to_encode = data.copy()
    access_token_expires = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": access_token_expires})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("sub")
        if id is None:
            raise credentials_exception
        token_data = auth_schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    user = crud.get_user(get_db, token_data.id)
    if user is None:
        raise credentials_exception
    return user

def get_current_user(token: str = Depends(oauth2_scheme), db: SessionLocal = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user = verify_token(token, credentials_exception)
    
    return user