"""
Helper functions for the application.
"""


def format_response(data: dict, message: str = None, status: str = "success") -> dict:
    """Format API response in a consistent manner."""
    return {"status": status, "message": message, "data": data}


def calculate_calorie_deficit(current_intake: int, goal_intake: int) -> int:
    """Calculate the calorie deficit or surplus."""
    return goal_intake - current_intake


def get_workout_recommendation(fitness_level: str, fitness_goal: str) -> dict:
    """Get basic workout recommendations based on fitness level and goal."""
    recommendations = {
        "Beginner": {
            "Weight Loss": "3 days per week, 45-60 minutes each, focus on cardio and light strength",
            "Muscle Gain": "3 days per week, 60 minutes each, focus on strength training",
            "Endurance": "3 days per week, mix of cardio and light strength",
            "Flexibility": "5 days per week, 30 minutes yoga/stretching",
            "General Fitness": "3-4 days per week, mix of cardio and strength",
        },
        "Moderately Active": {
            "Weight Loss": "4 days per week, 60 minutes each, mix of cardio and strength",
            "Muscle Gain": "4-5 days per week, 75 minutes each, focus on strength training",
            "Endurance": "4 days per week, progressive cardio",
            "Flexibility": "3-4 days per week, 45 minutes yoga/stretching",
            "General Fitness": "4 days per week, balanced routine",
        },
        "Very Active": {
            "Weight Loss": "5 days per week, 60-75 minutes each, high-intensity training",
            "Muscle Gain": "5-6 days per week, 90 minutes each, advanced strength training",
            "Endurance": "5-6 days per week, high-volume cardio",
            "Flexibility": "4 days per week, advanced yoga",
            "General Fitness": "5-6 days per week, advanced programs",
        },
    }

    return recommendations.get(fitness_level, {}).get(fitness_goal, "Consult a trainer")
