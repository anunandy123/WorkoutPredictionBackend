import requests
from sqlalchemy.orm import Session

from app.config.settings import settings
from app.models.food_model import Calories


def search_food_api(
    food_name: str, user_id: int, fitness_goal: str, db: Session
) -> dict:
    """
    Search for food in the calories table. If not found, query the external API.
    """
    # Check if food exists in database
    existing_food = (
        db.query(Calories).filter(Calories.name.ilike(f"%{food_name}%")).first()
    )

    if existing_food:
        return {
            "food_id": existing_food.food_id,
            "name": existing_food.name,
            "calories": float(existing_food.calories) if existing_food.calories else 0,
            "proteins": float(existing_food.proteins) if existing_food.proteins else 0,
            "fat": float(existing_food.fat) if existing_food.fat else 0,
            "carbs": float(existing_food.carbs) if existing_food.carbs else 0,
            "food_group": existing_food.food_group,
            "source": "database",
        }

    # If not in database, search external API
    try:
        api_url = "https://api.c0r.ai/v1/search"
        headers = {"X-API-Key": settings.food_api_key}
        params = {"q": food_name, "limit": 10, "lang": "en"}

        response = requests.get(api_url, headers=headers, params=params)
        response.raise_for_status()

        data = response.json()

        if data.get("results"):
            first_result = data["results"][0]
            nutrition = first_result.get("nutrition", {})

            # Store in database
            new_food = Calories(
                name=first_result.get("name", food_name),
                asked_by_user_id=user_id,
                fitness_goal=fitness_goal,
                calories=nutrition.get("calories", 0),
                proteins=nutrition.get("proteins", 0),
                fat=nutrition.get("fats", 0),
                carbs=nutrition.get("carbs", 0),
                food_group=first_result.get("food_group", "Unknown"),
            )
            db.add(new_food)
            db.commit()
            db.refresh(new_food)

            return {
                "food_id": new_food.food_id,
                "name": new_food.name,
                "calories": float(new_food.calories) if new_food.calories else 0,
                "proteins": float(new_food.proteins) if new_food.proteins else 0,
                "fat": float(new_food.fat) if new_food.fat else 0,
                "carbs": float(new_food.carbs) if new_food.carbs else 0,
                "food_group": new_food.food_group,
                "source": "api",
            }
        else:
            return {"error": "Food not found in API"}

    except Exception as e:
        return {"error": str(e)}
