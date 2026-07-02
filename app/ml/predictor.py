from app.ml.fitness_predictor import (
    predict_all,
    predict_calories,
    predict_diet,
    predict_exercise,
    predict_meal,
    predict_workout,
)


class Predictor:
    @staticmethod
    def predict_fitness(payload: dict) -> dict:
        return predict_all(payload)

    @staticmethod
    def predict_calories(payload: dict) -> dict:
        return predict_calories(payload)

    @staticmethod
    def predict_workout(payload: dict) -> dict:
        return predict_workout(payload)

    @staticmethod
    def predict_diet(payload: dict) -> dict:
        return predict_diet(payload)

    @staticmethod
    def predict_exercise(payload: dict) -> dict:
        return predict_exercise(payload)

    @staticmethod
    def predict_meal(payload: dict) -> dict:
        return predict_meal(payload)
