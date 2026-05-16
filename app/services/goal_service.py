from sqlalchemy.orm import Session
from app.repositories.goal_repository import GoalRepository
from app.schemas.goal_schema import GoalCreate, GoalResponse, GoalUpdate


class GoalService:
    @staticmethod
    def create_goal(db: Session, user_id: int, goal_data: GoalCreate) -> dict:
        """Create a new goal."""
        goal = GoalRepository.create_goal(db, user_id, goal_data)
        return GoalResponse.from_orm(goal).model_dump()

    @staticmethod
    def get_user_goals(db: Session, user_id: int) -> list:
        """Get all goals for a user."""
        goals = GoalRepository.get_user_goals(db, user_id)
        return [GoalResponse.from_orm(goal).model_dump() for goal in goals]

    @staticmethod
    def update_goal(db: Session, goal_id: int, goal_data: GoalUpdate) -> dict:
        """Update a goal."""
        goal = GoalRepository.update_goal(db, goal_id, goal_data)
        if not goal:
            return {"error": "Goal not found"}
        return GoalResponse.from_orm(goal).model_dump()

    @staticmethod
    def delete_goal(db: Session, goal_id: int) -> dict:
        """Delete a goal."""
        if GoalRepository.delete_goal(db, goal_id):
            return {"message": "Goal deleted successfully"}
        return {"error": "Goal not found"}
