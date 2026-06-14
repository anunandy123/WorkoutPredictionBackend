import pickle
import os
import json


# Paths


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")


# Load Models


def load(name):
    with open(os.path.join(MODEL_DIR, f"{name}.pkl"), "rb") as f:
        return pickle.load(f)

model_calories = load("calories_linear_regression")
scaler_calories = load("calories_scaler")
model_workout = load("workout_random_forest")
model_diet = load("diet_random_forest")
model_exercise = load("exercise_random_forest")
model_meal = load("meal_decision_tree")
encoders = load("label_encoders")

print("All models loaded.")


# Encoder Helpers


def enc(ns, val):
    le = encoders[ns]

    if val not in le.classes_:
        raise ValueError(
            f"Unknown '{val}' for {ns}. "
            f"Valid values: {list(le.classes_)}"
        )

    return le.transform([val])[0]


def dec(ns, val):
    return encoders[ns].inverse_transform([int(val)])[0]

# Main Prediction Function


def predict_all(user: dict) -> dict:

    age = user["age"]
    gender = enc("gym_Gender", user["gender"])
    weight = user["weight_kg"]
    bmi = user["bmi"]
    bpm = user["avg_bpm"]
    session = user["session_duration_hrs"]
    freq = user["workout_frequency_days_per_week"]
    exp = user["experience_level"]
    fatpct = user["fat_percentage"]
    proteins = user["proteins"]
    carbs = user["carbs"]
    fats = user["fats"]


    # 1. Calories Prediction


    X1 = scaler_calories.transform(
        [[weight, bpm, session, bmi, age]]
    )

    calories = round(
        float(model_calories.predict(X1)[0]),
        2
    )


    # 2. Workout Recommendation


    wo_enc = model_workout.predict(
        [[age, gender, bmi, bpm, session, exp, freq]]
    )[0]

    workout_type = dec("gym_Workout_Type", wo_enc)

  
    # 3. Diet Recommendation
   

    diet_enc = model_diet.predict(
        [[calories, proteins, fats, carbs, fatpct]]
    )[0]

    diet_type = dec("nutr_diet_type", diet_enc)

  
    # 4. Exercise Recommendation
   

    workout_type_map = {
        "Cardio": "Cardio",
        "Strength": "Strength",
        "HIIT": "Plyometrics",
        "Yoga": "Stretching",
        "Flexibility": "Stretching"
    }

    mapped_workout = workout_type_map.get(
        workout_type,
        "Strength"
    )

    exer_type = enc(
        "exer_Workout_Type",
        mapped_workout
    )

    exer_mu = enc(
        "exer_Muscle_Group",
        user.get("target_muscle_group", "Chest")
    )

    exer_eq = enc(
        "exer_Equipment",
        user.get("equipment", "Body Only")
    )

    exer_df = enc(
        "exer_Difficulty",
        user.get("difficulty_level", "Intermediate")
    )

    ex_enc = model_exercise.predict(
        [[exer_type, exer_mu, exer_eq, exer_df]]
    )[0]

    exercise = dec("exer_Name", ex_enc)

  
    # 5. Meal Recommendation
 

    meal_wo = enc(
        "meal_Workout_Type",
        workout_type
    )

    meal_enc = model_meal.predict(
        [[bmi, calories, meal_wo, proteins, carbs, fats]]
    )[0]

    meal_type = dec(
        "meal_meal_type",
        meal_enc
    )

    return {
        "calories_burned": calories,
        "workout_type": workout_type,
        "diet_type": diet_type,
        "exercise_name": exercise,
        "meal_type": meal_type
    }


# Test Run


if __name__ == "__main__":

    sample_user = {
        "age": 25,
        "gender": "Male",
        "weight_kg": 75.0,
        "bmi": 24.5,
        "avg_bpm": 140,
        "session_duration_hrs": 1.0,
        "workout_frequency_days_per_week": 4,
        "experience_level": 2,
        "fat_percentage": 18.0,
        "proteins": 150,
        "carbs": 250,
        "fats": 60,
        "target_muscle_group": "Chest",
        "equipment": "Barbell",
        "difficulty_level": "Intermediate"
    }

    result = predict_all(sample_user)

    print(json.dumps(result, indent=2))