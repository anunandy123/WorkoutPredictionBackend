from typing import Optional

from pydantic import BaseModel


class LifestyleCreate(BaseModel):
    sleep_hours: float
    stress_level: int
    water_intake: float
    sitting_hours: int


class LifestyleUpdate(BaseModel):
    sleep_hours: Optional[float] = None
    stress_level: Optional[int] = None
    water_intake: Optional[float] = None
    sitting_hours: Optional[int] = None


class LifestyleResponse(BaseModel):
    lifestyle_id: int
    user_id: int
    sleep_hours: float
    stress_level: int
    water_intake: float
    sitting_hours: int

    class Config:
        from_attributes = True
