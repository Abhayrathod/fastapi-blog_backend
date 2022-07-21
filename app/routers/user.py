from .. import models, utils, schemas
from fastapi import FastAPI, HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from .. database import get_db

router = APIRouter(
    prefix="/user",
    tags=['Users']
)

@router.post("",status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    email = db.query(models.User).filter(models.User.email == user.email).first()
    if email is not None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with email id {user.email} already exists")
    
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    # return f"User with email id {new_user.email} Created successfully"
    return new_user

@router.get("/{id}",response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    return user