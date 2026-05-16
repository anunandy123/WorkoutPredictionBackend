from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.utils.validators import validate_difficulty , validate_muscle_groups
from app.config.database import get_db
from app.config.security import get_current_user
from app.models.exercise_model import Exercise
from app.utils.constants import DIFFICULTY_LEVELS , MUSCLE_GROUPS , WORKOUT_DAYS , FITNESS_LEVELS , FITNESS_GOALS
from app.schemas.exercise_schema import ExerciseCreate, ExerciseResponse, ExerciseUpdate

router = APIRouter(prefix="/api/exercises", tags=["exercises"])


@router.post("/", response_model=ExerciseResponse)
def create_exercise(
    exercise_data: ExerciseCreate,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new exercise."""
    if not validate_difficulty(exercise_data.difficulty):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"difficulty can only be among {DIFFICULTY_LEVELS}"
        )
    if not validate_muscle_groups(exercise_data.muscle_group):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"muscle group can only be among {MUSCLE_GROUPS}"
        )

    db_exercise = Exercise(
        exercise_name=exercise_data.exercise_name,
        muscle_group=exercise_data.muscle_group,
        difficulty=exercise_data.difficulty,
        equipment_needed=exercise_data.equipment_needed,
    )
    db.add(db_exercise)
    db.commit()
    db.refresh(db_exercise)

    # Return ORM object → FastAPI will serialize via ExerciseResponse
    return db_exercise


@router.get("/", response_model=list[ExerciseResponse])
def get_exercises(db: Session = Depends(get_db)):
    """Get all exercises."""
    exercises = db.query(Exercise).all()
    return exercises


@router.get("/{exercise_id}", response_model=ExerciseResponse)
def get_exercise(exercise_id: int, db: Session = Depends(get_db)):
    """Get exercise by ID."""
    exercise = db.query(Exercise).filter(Exercise.exercise_id == exercise_id).first()
    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Exercise not found"
        )
    return exercise


@router.put("/{exercise_id}", response_model=ExerciseResponse)
def update_exercise(
    exercise_id: int,
    exercise_data: ExerciseUpdate,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update an exercise."""
    if not validate_difficulty(exercise_data.difficulty):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"difficulty can only be among {DIFFICULTY_LEVELS}"
        )
    if not validate_muscle_groups(exercise_data.muscle_group):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"muscle group can only be among {MUSCLE_GROUPS}"
        )

    exercise = db.query(Exercise).filter(Exercise.exercise_id == exercise_id).first()
    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Exercise not found"
        )

    update_data = exercise_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(exercise, key, value)

    db.commit()
    db.refresh(exercise)
    return exercise


@router.delete("/{exercise_id}")
def delete_exercise(
    exercise_id: int,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete an exercise."""
    exercise = db.query(Exercise).filter(Exercise.exercise_id == exercise_id).first()
    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Exercise not found"
        )

    db.delete(exercise)
    db.commit()
    return {"message": "Exercise deleted successfully"}
