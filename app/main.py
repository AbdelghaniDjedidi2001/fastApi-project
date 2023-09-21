from fastapi import FastAPI
from .models import Base 
from .database import engine  
from .routers.user import user 
from .routers.post import post


Base.metadata.create_all(bind=engine)


app = FastAPI()


app.include_router(user.router)
app.include_router(post.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}




