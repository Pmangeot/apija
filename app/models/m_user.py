from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    firstname: str
    lastname: str
    email: str    

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    password: Optional[str] = None
    admin: bool = False

class UserUpdate(UserBase):
    id: int

class UserPasswordUpdate(BaseModel):
    id: int
    old_password: str
    new_password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str