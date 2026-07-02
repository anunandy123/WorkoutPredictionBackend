from typing import Literal, Optional

from pydantic import BaseModel, Field, field_validator

from app.ml.model_loader import ModelLoader

Gender = Literal["Male", "Female"]
DifficultyLevel = Literal["Beginner", "Intermediate", "Expert"]
Equipment = Literal[
    "Barbell",
    "Dumbbell",
    "Body Only",
    "Cable",
    "Machine",
    "Kettlebells",
    "Bands",
    "Exercise Ball",
    "Foam Roll",
    "E-Z Curl Bar",
    "Medicine Ball",
    "Other",
]


def _validate_muscle_group(value: Optional[str]) -> Optional[str]:
    if value is None:
        return value
    valid_groups = ModelLoader.get_target_muscle_groups()
    if value not in valid_groups:
        raise ValueError(
            f"Invalid target_muscle_group. Valid values: {valid_groups}"
        )
    return value


def _validate_workout_type(value: str) -> str:
    valid_types = ModelLoader.get_encoder_classes("gym_Workout_Type")
    if value not in valid_types:
        raise ValueError(f"Invalid workout_type. Valid values: {valid_types}")
    return value


class CaloriePredictionRequest(BaseModel):
    age: int = Field(..., gt=0, le=120)
    weight_kg: float = Field(..., gt=0)
    avg_bpm: int = Field(..., gt=0)
    session_duration_hrs: float = Field(..., gt=0)
    bmi: float = Field(..., gt=0)


class CaloriePredictionResponse(BaseModel):
    calories_burned: float


class WorkoutPredictionRequest(BaseModel):
    age: int = Field(..., gt=0, le=120)
    gender: Gender
    bmi: float = Field(..., gt=0)
    avg_bpm: int = Field(..., gt=0)
    session_duration_hrs: float = Field(..., gt=0)
    experience_level: int = Field(
        ..., ge=1, le=3, description="1=Beginner, 2=Intermediate, 3=Expert"
    )
    workout_frequency_days_per_week: int = Field(..., ge=0, le=7)


class WorkoutPredictionResponse(BaseModel):
    workout_type: str


class DietPredictionRequest(BaseModel):
    calories: float = Field(..., gt=0)
    proteins: float = Field(..., ge=0)
    fats: float = Field(..., ge=0)
    carbs: float = Field(..., ge=0)
    fat_percentage: float = Field(..., ge=0)


class DietPredictionResponse(BaseModel):
    diet_type: str


class ExercisePredictionRequest(BaseModel):
    workout_type: str
    target_muscle_group: Optional[str] = "Chest"
    equipment: Optional[Equipment] = "Body Only"
    difficulty_level: Optional[DifficultyLevel] = "Intermediate"

    @field_validator("workout_type")
    @classmethod
    def validate_workout_type(cls, value: str) -> str:
        return _validate_workout_type(value)

    @field_validator("target_muscle_group")
    @classmethod
    def validate_target_muscle_group(cls, value: Optional[str]) -> Optional[str]:
        return _validate_muscle_group(value)


class ExercisePredictionResponse(BaseModel):
    exercise_name: str


class MealPredictionRequest(BaseModel):
    bmi: float = Field(..., gt=0)
    calories_burned: float = Field(..., gt=0)
    workout_type: str
    proteins: float = Field(..., ge=0)
    carbs: float = Field(..., ge=0)
    fats: float = Field(..., ge=0)

    @field_validator("workout_type")
    @classmethod
    def validate_workout_type(cls, value: str) -> str:
        return _validate_workout_type(value)


class MealPredictionResponse(BaseModel):
    meal_type: str


class FitnessPredictionRequest(BaseModel):
    age: int = Field(..., gt=0, le=120)
    gender: Gender
    weight_kg: float = Field(..., gt=0)
    bmi: float = Field(..., gt=0)
    avg_bpm: int = Field(..., gt=0)
    session_duration_hrs: float = Field(..., gt=0)
    workout_frequency_days_per_week: int = Field(..., ge=0, le=7)
    experience_level: int = Field(
        ..., ge=1, le=3, description="1=Beginner, 2=Intermediate, 3=Expert"
    )
    fat_percentage: float = Field(..., ge=0)
    proteins: float = Field(..., ge=0)
    carbs: float = Field(..., ge=0)
    fats: float = Field(..., ge=0)
    target_muscle_group: Optional[str] = "Chest"
    equipment: Optional[Equipment] = "Body Only"
    difficulty_level: Optional[DifficultyLevel] = "Intermediate"

    @field_validator("target_muscle_group")
    @classmethod
    def validate_target_muscle_group(cls, value: Optional[str]) -> Optional[str]:
        return _validate_muscle_group(value)


class FitnessPredictionResponse(BaseModel):
    calories_burned: float
    workout_type: str
    diet_type: str
    exercise_name: str
    meal_type: str


class PredictionOptionsResponse(BaseModel):
    gender: list[str]
    equipment: list[str]
    difficulty_level: list[str]
    target_muscle_group: list[str]
    workout_type: list[str]
    experience_level: dict[int, str]
