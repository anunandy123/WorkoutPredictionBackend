from sqlalchemy.orm import Session

from app.repositories.workout_repository import WorkoutRepository
from app.schemas.workout_schema import (
    WorkoutPlanCreate,
    WorkoutPlanResponse,
    WorkoutPlanUpdate,
)


class WorkoutService:
    @staticmethod
    def create_workout_plan(
        db: Session, user_id: int, plan_data: WorkoutPlanCreate
    ) -> dict:
        """Create a new workout plan."""
        plan = WorkoutRepository.create_workout_plan(db, user_id, plan_data)
        return WorkoutPlanResponse.from_orm(plan).model_dump()

    @staticmethod
    def get_user_workout_plans(db: Session, user_id: int) -> list:
        """Get all workout plans for a user."""
        plans = WorkoutRepository.get_user_workout_plans(db, user_id)
        return [WorkoutPlanResponse.from_orm(plan).model_dump() for plan in plans]

    @staticmethod
    def update_workout_plan(
        db: Session, plan_id: int, plan_data: WorkoutPlanUpdate
    ) -> dict:
        """Update a workout plan."""
        plan = WorkoutRepository.update_workout_plan(db, plan_id, plan_data)
        if not plan:
            return {"error": "Workout plan not found"}
        return WorkoutPlanResponse.from_orm(plan).model_dump()

    @staticmethod
    def delete_workout_plan(db: Session, plan_id: int) -> dict:
        """Delete a workout plan."""
        if WorkoutRepository.delete_workout_plan(db, plan_id):
            return {"message": "Workout plan deleted successfully"}
        return {"error": "Workout plan not found"}
