from typing import Optional

from pydantic import BaseModel


class GoalCreate(BaseModel):
    fitness_goal: str
    target_weight: int
    workout_days: int
    workout_minutes: int


class GoalUpdate(BaseModel):
    fitness_goal: Optional[str] = None
    target_weight: Optional[int] = None
    workout_days: Optional[int] = None
    workout_minutes: Optional[int] = None


class GoalResponse(BaseModel):
    goal_id: int
    user_id: int
    fitness_goal: str
    target_weight: int
    workout_days: int
    workout_minutes: int

    class Config:
        from_attributes = True
