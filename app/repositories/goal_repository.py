from sqlalchemy.orm import Session

from app.models.goal_model import Goal
from app.schemas.goal_schema import GoalCreate, GoalUpdate


class GoalRepository:
    @staticmethod
    def create_goal(db: Session, user_id: int, goal_data: GoalCreate) -> Goal:
        """Create a new goal for a user."""
        db_goal = Goal(
            user_id=user_id,
            fitness_goal=goal_data.fitness_goal,
            target_weight=goal_data.target_weight,
            workout_days=goal_data.workout_days,
            workout_minutes=goal_data.workout_minutes,
        )
        db.add(db_goal)
        db.commit()
        db.refresh(db_goal)
        return db_goal

    @staticmethod
    def get_goal_by_id(db: Session, goal_id: int) -> Goal:
        """Get goal by ID."""
        return db.query(Goal).filter(Goal.goal_id == goal_id).first()

    @staticmethod
    def get_user_goals(db: Session, user_id: int) -> list:
        """Get all goals for a user."""
        return db.query(Goal).filter(Goal.user_id == user_id).all()

    @staticmethod
    def update_goal(db: Session, goal_id: int, goal_data: GoalUpdate) -> Goal:
        """Update a goal."""
        db_goal = GoalRepository.get_goal_by_id(db, goal_id)
        if db_goal:
            update_data = goal_data.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_goal, key, value)
            db.commit()
            db.refresh(db_goal)
        return db_goal

    @staticmethod
    def delete_goal(db: Session, goal_id: int) -> bool:
        """Delete a goal."""
        db_goal = GoalRepository.get_goal_by_id(db, goal_id)
        if db_goal:
            db.delete(db_goal)
            db.commit()
            return True
        return False
