from typing import List

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    addresses: List[EmailStr]


class UserCreate(UserBase):
    password1: str
    password2: str


class UserUpdate(UserBase):
    pass


class Token(BaseModel):
    token_type: str
    user: dict
    exp: int
    iat: int
