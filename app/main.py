from typing import List

from app.routers.vote import vote
from . import models
from .database import engine, SessionLocal, get_db
from typing import Optional
from urllib import response
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from random import randrange
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .routers import post, user, auth, vote
from .config import settings

# models.Base.metadata.create_all(bind=engine)          ## if alembic is there then you don't need these however
                                                            ## these doesnt break anything

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def return_message():
    return {"message":"This is backend back2biz"}