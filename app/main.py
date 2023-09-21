from fastapi import FastAPI
from .models import Base 
from .database import engine  
from .routers.user import user 
from .routers.post import post
from .routers.auth import auth


Base.metadata.create_all(bind=engine)


app = FastAPI()


app.include_router(user.router)
app.include_router(post.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}




