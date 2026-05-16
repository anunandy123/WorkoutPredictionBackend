from sqlalchemy.orm import Session

from app.utils.calorie import search_food_api


class CalorieService:
    @staticmethod
    def search_food(
        db: Session, food_name: str, user_id: int, fitness_goal: str
    ) -> dict:
        """Search for food and get nutritional information."""
        result = search_food_api(food_name, user_id, fitness_goal, db)
        return result

    @staticmethod
    def get_food_by_name(db: Session, food_name: str) -> dict:
        """Get food information from the database."""
        from app.models.food_model import Calories

        food = db.query(Calories).filter(Calories.name.ilike(f"%{food_name}%")).first()

        if food:
            return {
                "food_id": food.food_id,
                "name": food.name,
                "calories": float(food.calories) if food.calories else 0,
                "proteins": float(food.proteins) if food.proteins else 0,
                "fat": float(food.fat) if food.fat else 0,
                "carbs": float(food.carbs) if food.carbs else 0,
                "food_group": food.food_group,
            }
        return {"error": "Food not found"}
