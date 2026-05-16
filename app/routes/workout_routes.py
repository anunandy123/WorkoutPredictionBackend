from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.config.security import get_current_user
from app.schemas.workout_schema import (
    WorkoutPlanCreate,
    WorkoutPlanResponse,
    WorkoutPlanUpdate,
)
from app.services.workout_service import WorkoutService

router = APIRouter(prefix="/api/workouts", tags=["workouts"])


@router.post("/", response_model=WorkoutPlanResponse)
def create_workout_plan(
    plan_data: WorkoutPlanCreate,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new workout plan."""
    result = WorkoutService.create_workout_plan(db, user_id, plan_data)
    return result


@router.get("/", response_model=list)
def get_workout_plans(
    user_id: int = Depends(get_current_user), db: Session = Depends(get_db)
):
    """Get all workout plans for the current user."""
    return WorkoutService.get_user_workout_plans(db, user_id)


@router.put("/{plan_id}", response_model=WorkoutPlanResponse)
def update_workout_plan(
    plan_id: int,
    plan_data: WorkoutPlanUpdate,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update a workout plan."""
    result = WorkoutService.update_workout_plan(db, plan_id, plan_data)

    if "error" in result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=result["error"]
        )

    return result


@router.delete("/{plan_id}")
def delete_workout_plan(
    plan_id: int,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a workout plan."""
    result = WorkoutService.delete_workout_plan(db, plan_id)

    if "error" in result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=result["error"]
        )

    return result
