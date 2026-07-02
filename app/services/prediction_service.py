from app.ml.model_loader import ModelLoader
from app.ml.predictor import Predictor
from app.schemas.prediction_schema import (
    CaloriePredictionRequest,
    DietPredictionRequest,
    ExercisePredictionRequest,
    FitnessPredictionRequest,
    MealPredictionRequest,
    WorkoutPredictionRequest,
)
from app.utils.constants import EQUIPMENT_OPTIONS, EXPERIENCE_LEVELS


class PredictionService:
    @staticmethod
    def predict(payload: FitnessPredictionRequest) -> dict:
        return Predictor.predict_fitness(payload.model_dump())

    @staticmethod
    def predict_calories(payload: CaloriePredictionRequest) -> dict:
        return Predictor.predict_calories(payload.model_dump())

    @staticmethod
    def predict_workout(payload: WorkoutPredictionRequest) -> dict:
        return Predictor.predict_workout(payload.model_dump())

    @staticmethod
    def predict_diet(payload: DietPredictionRequest) -> dict:
        return Predictor.predict_diet(payload.model_dump())

    @staticmethod
    def predict_exercise(payload: ExercisePredictionRequest) -> dict:
        return Predictor.predict_exercise(payload.model_dump())

    @staticmethod
    def predict_meal(payload: MealPredictionRequest) -> dict:
        return Predictor.predict_meal(payload.model_dump())

    @staticmethod
    def get_prediction_options() -> dict:
        encoders = ModelLoader.get_encoders()
        return {
            "gender": list(encoders["gym_Gender"].classes_),
            "equipment": EQUIPMENT_OPTIONS,
            "difficulty_level": list(encoders["exer_Difficulty"].classes_),
            "target_muscle_group": list(encoders["exer_Muscle_Group"].classes_),
            "workout_type": list(encoders["gym_Workout_Type"].classes_),
            "experience_level": EXPERIENCE_LEVELS,
        }
