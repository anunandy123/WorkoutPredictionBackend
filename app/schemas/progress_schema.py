from datetime import date
from typing import Optional

from pydantic import BaseModel


class ProgressCreate(BaseModel):
    weight: float
    calories_consumed: int
    workout_completed: bool
    energy_level: int


class ProgressUpdate(BaseModel):
    weight: Optional[float] = None
    calories_consumed: Optional[int] = None
    workout_completed: Optional[bool] = None
    energy_level: Optional[int] = None


class ProgressResponse(BaseModel):
    progress_id: int
    user_id: int
    weight: float
    calories_consumed: int
    workout_completed: bool
    energy_level: int
    tracked_on: date

    class Config:
        from_attributes = True
