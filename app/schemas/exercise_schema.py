from typing import Optional

from pydantic import BaseModel


class ExerciseCreate(BaseModel):
    exercise_name: str
    muscle_group: str
    difficulty: str
    equipment_needed: str


class ExerciseUpdate(BaseModel):
    exercise_name: Optional[str] = None
    muscle_group: Optional[str] = None
    difficulty: Optional[str] = None
    equipment_needed: Optional[str] = None


class ExerciseResponse(BaseModel):
    exercise_id: int
    exercise_name: str
    muscle_group: str
    difficulty: str
    equipment_needed: str
    model_config = {
        "from_attributes": True
    }
