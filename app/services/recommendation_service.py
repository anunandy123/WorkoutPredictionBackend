from sqlalchemy.orm import Session

from app.repositories.goal_repository import GoalRepository
from app.repositories.user_repository import UserRepository
from app.utils.bmi import calculate_bmi
from app.utils.helpers import get_workout_recommendation


class RecommendationService:
    @staticmethod
    def get_personalized_recommendations(db: Session, user_id: int) -> dict:
        """Get personalized recommendations based on user profile and goals."""
        user = UserRepository.get_user_by_id(db, user_id)

        if not user:
            return {"error": "User not found"}

        goals = GoalRepository.get_user_goals(db, user_id)

        recommendations = {
            "user_name": user.name,
            "bmi": (
                calculate_bmi(user.weight, user.height)
                if user.weight and user.height
                else "N/A"
            ),
            "current_fitness_level": user.fitness_level,
            "goals": [],
        }

        for goal in goals:
            workout_rec = get_workout_recommendation(
                user.fitness_level, goal.fitness_goal
            )
            recommendations["goals"].append(
                {
                    "fitness_goal": goal.fitness_goal,
                    "target_weight": goal.target_weight,
                    "workout_days": goal.workout_days,
                    "workout_minutes": goal.workout_minutes,
                    "recommendation": workout_rec,
                }
            )

        return recommendations

    @staticmethod
    def get_nutrition_recommendations(db: Session, user_id: int) -> dict:
        """Get nutrition recommendations based on user profile."""
        user = UserRepository.get_user_by_id(db, user_id)

        if not user:
            return {"error": "User not found"}

        # Calculate basic nutritional needs (dummy calculation)
        # In production, this would use ML models
        daily_calorie_goal = 2000  # Default
        protein_goal = 0.8 * user.weight if user.weight else 0  # grams per kg

        return {
            "user_name": user.name,
            "estimated_daily_calories": daily_calorie_goal,
            "protein_goal_grams": protein_goal,
            "nutrition_tips": [
                "Drink at least 2-3 liters of water daily",
                "Eat protein with every meal",
                "Include vegetables in every meal",
                "Avoid processed foods",
            ],
        }
