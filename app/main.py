from typing import List
from . import models
from .database import engine, SessionLocal, get_db
from typing import Optional
from urllib import response
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from random import randrange
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)