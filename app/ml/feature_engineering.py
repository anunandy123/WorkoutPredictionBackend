"""
Feature engineering module for preparing data for ML models.
"""

from app.schemas.prediction_schema import (
    CaloriePredictionRequest,
    DietPredictionRequest,
    ExercisePredictionRequest,
    FitnessPredictionRequest,
    MealPredictionRequest,
    WorkoutPredictionRequest,
)


class FeatureEngineering:
    @staticmethod
    def prepare_calorie_features(payload: CaloriePredictionRequest) -> dict:
        return payload.model_dump()

    @staticmethod
    def prepare_workout_features(payload: WorkoutPredictionRequest) -> dict:
        return payload.model_dump()

    @staticmethod
    def prepare_diet_features(payload: DietPredictionRequest) -> dict:
        return payload.model_dump()

    @staticmethod
    def prepare_exercise_features(payload: ExercisePredictionRequest) -> dict:
        return payload.model_dump()

    @staticmethod
    def prepare_meal_features(payload: MealPredictionRequest) -> dict:
        return payload.model_dump()

    @staticmethod
    def prepare_prediction_features(payload: FitnessPredictionRequest) -> dict:
        return payload.model_dump()
