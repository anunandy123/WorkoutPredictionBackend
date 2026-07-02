import os
import pickle
from functools import lru_cache
from typing import Any

from app.utils.constants import MUSCLE_GROUPS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")


def _load_pickle(name: str) -> Any:
    path = os.path.join(MODEL_DIR, f"{name}.pkl")
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Model file not found: {path}")
    with open(path, "rb") as f:
        return pickle.load(f)


@lru_cache(maxsize=1)
def load_all_models() -> dict[str, Any]:
    return {
        "model_calories": _load_pickle("calories_linear_regression"),
        "scaler_calories": _load_pickle("calories_scaler"),
        "model_workout": _load_pickle("workout_random_forest"),
        "model_diet": _load_pickle("diet_random_forest"),
        "model_exercise": _load_pickle("exercise_random_forest"),
        "model_meal": _load_pickle("meal_decision_tree"),
        "encoders": _load_pickle("label_encoders"),
    }


class ModelLoader:
    @staticmethod
    def get_models() -> dict[str, Any]:
        return load_all_models()

    @staticmethod
    def get_encoders() -> dict[str, Any]:
        return load_all_models()["encoders"]

    @staticmethod
    def get_encoder_classes(namespace: str) -> list:
        encoders = ModelLoader.get_encoders()
        if namespace not in encoders:
            raise KeyError(f"Encoder namespace '{namespace}' not found")
        return list(encoders[namespace].classes_)

    @staticmethod
    def get_target_muscle_groups() -> list[str]:
        try:
            return ModelLoader.get_encoder_classes("exer_Muscle_Group")
        except (FileNotFoundError, KeyError):
            return MUSCLE_GROUPS.copy()
