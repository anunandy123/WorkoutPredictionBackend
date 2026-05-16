from typing import Optional

from pydantic import BaseModel, EmailStr


class UserRegister(BaseModel):
    name: str
    password: str
    age: Optional[int] = None
    gender: Optional[str] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    fitness_level: Optional[str] = None


class UserLogin(BaseModel):
    name: str
    password: str


class UserResponse(BaseModel):
    user_id: int
    name: str
    age: Optional[int] = None
    gender: Optional[str] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    fitness_level: Optional[str] = None

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    fitness_level: Optional[str] = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user_id: int
