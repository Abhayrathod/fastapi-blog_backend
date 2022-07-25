from pydantic import BaseModel, EmailStr
from typing import Optional
from pydantic.types import conint

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass


#---------------------RESPONSE MODEL
class PostResponse(BaseModel):
    title: str
    published: bool
    owner_id: int

    class Config:
        orm_mode = True
        
        
#----------------------USER
class User(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    email: EmailStr

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)