from app.ml.model_loader import ModelLoader


def enc(ns: str, val: str) -> int:
    encoders = ModelLoader.get_encoders()
    le = encoders[ns]

    if val not in le.classes_:
        raise ValueError(
            f"Unknown '{val}' for {ns}. Valid values: {list(le.classes_)}"
        )

    return le.transform([val])[0]


def dec(ns: str, val: int) -> str:
    encoders = ModelLoader.get_encoders()
    return encoders[ns].inverse_transform([int(val)])[0]


WORKOUT_TYPE_MAP = {
    "Cardio": "Cardio",
    "Strength": "Strength",
    "HIIT": "Plyometrics",
    "Yoga": "Stretching",
    "Flexibility": "Stretching",
}


def predict_calories(payload: dict) -> dict:
    models = ModelLoader.get_models()
    X = models["scaler_calories"].transform(
        [
            [
                payload["weight_kg"],
                payload["avg_bpm"],
                payload["session_duration_hrs"],
                payload["bmi"],
                payload["age"],
            ]
        ]
    )
    calories = round(float(models["model_calories"].predict(X)[0]), 2)
    return {"calories_burned": calories}


def predict_workout(payload: dict) -> dict:
    models = ModelLoader.get_models()
    gender = enc("gym_Gender", payload["gender"])
    wo_enc = models["model_workout"].predict(
        [
            [
                payload["age"],
                gender,
                payload["bmi"],
                payload["avg_bpm"],
                payload["session_duration_hrs"],
                payload["experience_level"],
                payload["workout_frequency_days_per_week"],
            ]
        ]
    )[0]
    return {"workout_type": dec("gym_Workout_Type", wo_enc)}


def predict_diet(payload: dict) -> dict:
    models = ModelLoader.get_models()
    diet_enc = models["model_diet"].predict(
        [
            [
                payload["calories"],
                payload["proteins"],
                payload["fats"],
                payload["carbs"],
                payload["fat_percentage"],
            ]
        ]
    )[0]
    return {"diet_type": dec("nutr_diet_type", diet_enc)}


def predict_exercise(payload: dict) -> dict:
    models = ModelLoader.get_models()
    workout_type = payload["workout_type"]
    mapped_workout = WORKOUT_TYPE_MAP.get(workout_type, "Strength")

    ex_enc = models["model_exercise"].predict(
        [
            [
                enc("exer_Workout_Type", mapped_workout),
                enc(
                    "exer_Muscle_Group",
                    payload.get("target_muscle_group", "Chest"),
                ),
                enc("exer_Equipment", payload.get("equipment", "Body Only")),
                enc(
                    "exer_Difficulty",
                    payload.get("difficulty_level", "Intermediate"),
                ),
            ]
        ]
    )[0]
    return {"exercise_name": dec("exer_Name", ex_enc)}


def predict_meal(payload: dict) -> dict:
    models = ModelLoader.get_models()
    meal_enc = models["model_meal"].predict(
        [
            [
                payload["bmi"],
                payload["calories_burned"],
                enc("meal_Workout_Type", payload["workout_type"]),
                payload["proteins"],
                payload["carbs"],
                payload["fats"],
            ]
        ]
    )[0]
    return {"meal_type": dec("meal_meal_type", meal_enc)}


def predict_all(user: dict) -> dict:
    calories_result = predict_calories(user)
    calories = calories_result["calories_burned"]

    workout_result = predict_workout(user)
    workout_type = workout_result["workout_type"]

    diet_result = predict_diet(
        {
            "calories": calories,
            "proteins": user["proteins"],
            "fats": user["fats"],
            "carbs": user["carbs"],
            "fat_percentage": user["fat_percentage"],
        }
    )

    exercise_result = predict_exercise(
        {
            "workout_type": workout_type,
            "target_muscle_group": user.get("target_muscle_group", "Chest"),
            "equipment": user.get("equipment", "Body Only"),
            "difficulty_level": user.get("difficulty_level", "Intermediate"),
        }
    )

    meal_result = predict_meal(
        {
            "bmi": user["bmi"],
            "calories_burned": calories,
            "workout_type": workout_type,
            "proteins": user["proteins"],
            "carbs": user["carbs"],
            "fats": user["fats"],
        }
    )

    return {
        "calories_burned": calories,
        "workout_type": workout_type,
        "diet_type": diet_result["diet_type"],
        "exercise_name": exercise_result["exercise_name"],
        "meal_type": meal_result["meal_type"],
    }
