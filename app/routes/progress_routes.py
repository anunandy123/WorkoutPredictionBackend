from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.config.security import get_current_user
from app.models.progress_model import DailyProgress
from app.schemas.progress_schema import ProgressCreate, ProgressResponse, ProgressUpdate

router = APIRouter(prefix="/api/progress", tags=["progress"])


@router.post("/", response_model=ProgressResponse)
def log_progress(
    progress_data: ProgressCreate,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Log daily progress."""
    db_progress = DailyProgress(
        user_id=user_id,
        weight=progress_data.weight,
        calories_consumed=progress_data.calories_consumed,
        workout_completed=progress_data.workout_completed,
        energy_level=progress_data.energy_level,
        tracked_on=date.today(),
    )
    db.add(db_progress)
    db.commit()
    db.refresh(db_progress)
    return db_progress


@router.get("/", response_model=list)
def get_progress(
    user_id: int = Depends(get_current_user), db: Session = Depends(get_db)
):
    """Get user's progress logs."""
    progress = db.query(DailyProgress).filter(DailyProgress.user_id == user_id).all()
    return progress


@router.get("/{date_str}", response_model=ProgressResponse)
def get_progress_by_date(
    date_str: str,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get progress for a specific date."""
    try:
        target_date = date.fromisoformat(date_str)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid date format. Use YYYY-MM-DD",
        )

    progress = (
        db.query(DailyProgress)
        .filter(
            DailyProgress.user_id == user_id, DailyProgress.tracked_on == target_date
        )
        .first()
    )

    if not progress:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No progress found for this date",
        )

    return progress


@router.put("/{progress_id}", response_model=ProgressResponse)
def update_progress(
    progress_id: int,
    progress_data: ProgressUpdate,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update progress entry."""
    progress = (
        db.query(DailyProgress)
        .filter(
            DailyProgress.progress_id == progress_id, DailyProgress.user_id == user_id
        )
        .first()
    )

    if not progress:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Progress not found"
        )

    update_data = progress_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(progress, key, value)

    db.commit()
    db.refresh(progress)
    return progress


@router.delete("/{progress_id}")
def delete_progress(
    progress_id: int,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a progress entry."""
    progress = (
        db.query(DailyProgress)
        .filter(
            DailyProgress.progress_id == progress_id, DailyProgress.user_id == user_id
        )
        .first()
    )

    if not progress:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Progress not found"
        )

    db.delete(progress)
    db.commit()
    return {"message": "Progress entry deleted successfully"}
