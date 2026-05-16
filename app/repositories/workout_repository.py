from sqlalchemy.orm import Session

from app.models.workout_model import WorkoutPlan
from app.schemas.workout_schema import WorkoutPlanCreate, WorkoutPlanUpdate


class WorkoutRepository:
    @staticmethod
    def create_workout_plan(
        db: Session, user_id: int, plan_data: WorkoutPlanCreate
    ) -> WorkoutPlan:
        """Create a new workout plan."""
        db_plan = WorkoutPlan(
            user_id=user_id,
            workout_day=plan_data.workout_day,
            exercise_id=plan_data.exercise_id,
            sets=plan_data.sets,
            reps=plan_data.reps,
        )
        db.add(db_plan)
        db.commit()
        db.refresh(db_plan)
        return db_plan

    @staticmethod
    def get_workout_plan(db: Session, plan_id: int) -> WorkoutPlan:
        """Get workout plan by ID."""
        return db.query(WorkoutPlan).filter(WorkoutPlan.plan_id == plan_id).first()

    @staticmethod
    def get_user_workout_plans(db: Session, user_id: int) -> list:
        """Get all workout plans for a user."""
        return db.query(WorkoutPlan).filter(WorkoutPlan.user_id == user_id).all()

    @staticmethod
    def update_workout_plan(
        db: Session, plan_id: int, plan_data: WorkoutPlanUpdate
    ) -> WorkoutPlan:
        """Update a workout plan."""
        db_plan = WorkoutRepository.get_workout_plan(db, plan_id)
        if db_plan:
            update_data = plan_data.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_plan, key, value)
            db.commit()
            db.refresh(db_plan)
        return db_plan

    @staticmethod
    def delete_workout_plan(db: Session, plan_id: int) -> bool:
        """Delete a workout plan."""
        db_plan = WorkoutRepository.get_workout_plan(db, plan_id)
        if db_plan:
            db.delete(db_plan)
            db.commit()
            return True
        return False
