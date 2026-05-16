from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.config.security import get_current_user
from app.models.food_model import FoodLog
from app.schemas.food_schema import CalorieResponse, FoodLogCreate, FoodLogResponse
from app.services.calorie_service import CalorieService

router = APIRouter(prefix="/api/food", tags=["food"])


@router.post("/log", response_model=FoodLogResponse)
def log_food(
    food_data: FoodLogCreate,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Log food intake."""
    db_food_log = FoodLog(
        user_id=user_id,
        food_name=food_data.food_name,
        calories=food_data.calories,
        protein=food_data.protein,
        logged_at=datetime.utcnow(),
    )
    db.add(db_food_log)
    db.commit()
    db.refresh(db_food_log)
    return db_food_log


@router.get("/search/{food_name}", response_model=dict)
def search_food(
    food_name: str,
    fitness_goal: str = "General Fitness",
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Search for food by name and get nutritional information."""
    result = CalorieService.search_food(db, food_name, user_id, fitness_goal)

    if "error" in result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=result["error"]
        )

    return result


@router.get("/info/{food_name}", response_model=dict)
def get_food_info(food_name: str, db: Session = Depends(get_db)):
    """Get food nutritional information from database."""
    result = CalorieService.get_food_by_name(db, food_name)

    if "error" in result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=result["error"]
        )

    return result


@router.get("/logs", response_model=list)
def get_food_logs(
    user_id: int = Depends(get_current_user), db: Session = Depends(get_db)
):
    """Get user's food logs."""
    logs = db.query(FoodLog).filter(FoodLog.user_id == user_id).all()
    return logs


@router.delete("/log/{log_id}")
def delete_food_log(
    log_id: int, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)
):
    """Delete a food log entry."""
    log = (
        db.query(FoodLog)
        .filter(FoodLog.food_log_id == log_id, FoodLog.user_id == user_id)
        .first()
    )

    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Food log not found"
        )

    db.delete(log)
    db.commit()
    return {"message": "Food log deleted successfully"}
