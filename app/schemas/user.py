from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional


class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True