from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class FoodLogCreate(BaseModel):
    food_name: str
    calories: int
    protein: int


class FoodLogResponse(BaseModel):
    food_log_id: int
    user_id: int
    food_name: str
    calories: int
    protein: int
    logged_at: datetime

    class Config:
        from_attributes = True


class CalorieCreate(BaseModel):
    name: str
    fitness_goal: str
    calories: float
    proteins: float
    fat: float
    carbs: float
    food_group: str


class CalorieResponse(BaseModel):
    food_id: int
    name: str
    fitness_goal: str
    calories: float
    proteins: float
    fat: float
    carbs: float
    food_group: str

    class Config:
        from_attributes = True
