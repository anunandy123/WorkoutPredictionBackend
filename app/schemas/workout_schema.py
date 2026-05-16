from typing import Optional

from pydantic import BaseModel


class WorkoutPlanCreate(BaseModel):
    workout_day: str
    exercise_id: int
    sets: int
    reps: int


class WorkoutPlanUpdate(BaseModel):
    workout_day: Optional[str] = None
    exercise_id: Optional[int] = None
    sets: Optional[int] = None
    reps: Optional[int] = None


class WorkoutPlanResponse(BaseModel):
    plan_id: int
    user_id: int
    workout_day: str
    exercise_id: int
    sets: int
    reps: int

    class Config:
        from_attributes = True
