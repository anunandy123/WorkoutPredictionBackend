from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.utils.validators import validate_workout_days , validate_weight , validate_fitness_goals
from app.config.database import get_db
from app.config.security import get_current_user
from app.schemas.goal_schema import GoalCreate, GoalResponse, GoalUpdate
from app.services.goal_service import GoalService
from app.utils.constants import DIFFICULTY_LEVELS , MUSCLE_GROUPS , WORKOUT_DAYS , FITNESS_LEVELS , FITNESS_GOALS
router = APIRouter(prefix="/api/goals", tags=["goals"])


@router.post("/", response_model=GoalResponse)
def create_goal(
    goal_data: GoalCreate,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new goal."""
    if not validate_workout_days(goal_data.workout_days):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="work out days must be any number 7 to 1",
        )
    if not validate_weight(goal_data.target_weight):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Weights must be resonable - number from 20 to 200",
        )
    if not validate_fitness_goals(goal_data.fitness_goal):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"fitness goals can only be among {FITNESS_GOALS}"
        )

    result = GoalService.create_goal(db, user_id, goal_data)
    return result


@router.get("/", response_model=list)
def get_goals(user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get all goals for the current user."""
    return GoalService.get_user_goals(db, user_id)


@router.put("/{goal_id}", response_model=GoalResponse)
def update_goal(
    goal_id: int,
    goal_data: GoalUpdate,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update a goal."""
    if not validate_workout_days(goal_data.workout_days):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="work out days must be any number 7 to 1",
        )
    if not validate_weight(goal_data.target_weight):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Weights must be resonable - number from 20 to 200",
        )
    if not validate_fitness_goals(goal_data.fitness_goal):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"fitness goals can only be among {FITNESS_GOALS}"
        )
    result = GoalService.update_goal(db, goal_id, goal_data)
    if "error" in result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=result["error"]
        )

    return result


@router.delete("/{goal_id}")
def delete_goal(
    goal_id: int,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a goal."""
    result = GoalService.delete_goal(db, goal_id)

    if "error" in result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=result["error"]
        )

    return result
