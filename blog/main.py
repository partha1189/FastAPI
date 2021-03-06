from typing import List
from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schemas, models 
from .database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from .hashing import Hash
from .routers import blog, user


app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(blog.router)
app.include_router(user.router)

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

