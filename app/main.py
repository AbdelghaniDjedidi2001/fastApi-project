from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .models import Base 
from .database import engine  
from .routers.user import user 
from .routers.post import post
from .routers.auth import auth
from .routers.vote import vote
from .config import settings



Base.metadata.create_all(bind=engine)


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(post.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}




