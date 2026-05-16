from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.config.security import get_current_user
from app.models.lifestyle_model import Lifestyle
from app.schemas.lifestyle_schema import (
    LifestyleCreate,
    LifestyleResponse,
    LifestyleUpdate,
)

router = APIRouter(prefix="/api/lifestyle", tags=["lifestyle"])


@router.post("/", response_model=LifestyleResponse)
def create_lifestyle(
    lifestyle_data: LifestyleCreate,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create lifestyle entry for user."""
    db_lifestyle = Lifestyle(
        user_id=user_id,
        sleep_hours=lifestyle_data.sleep_hours,
        stress_level=lifestyle_data.stress_level,
        water_intake=lifestyle_data.water_intake,
        sitting_hours=lifestyle_data.sitting_hours,
    )
    db.add(db_lifestyle)
    db.commit()
    db.refresh(db_lifestyle)
    return db_lifestyle


@router.get("/", response_model=LifestyleResponse)
def get_lifestyle(
    user_id: int = Depends(get_current_user), db: Session = Depends(get_db)
):
    """Get user's lifestyle information."""
    lifestyle = db.query(Lifestyle).filter(Lifestyle.user_id == user_id).first()
    if not lifestyle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Lifestyle data not found"
        )
    return lifestyle


@router.put("/", response_model=LifestyleResponse)
def update_lifestyle(
    lifestyle_data: LifestyleUpdate,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update user's lifestyle information."""
    lifestyle = db.query(Lifestyle).filter(Lifestyle.user_id == user_id).first()
    if not lifestyle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Lifestyle data not found"
        )

    update_data = lifestyle_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(lifestyle, key, value)

    db.commit()
    db.refresh(lifestyle)
    return lifestyle


@router.delete("/")
def delete_lifestyle(
    user_id: int = Depends(get_current_user), db: Session = Depends(get_db)
):
    """Delete user's lifestyle information."""
    lifestyle = db.query(Lifestyle).filter(Lifestyle.user_id == user_id).first()
    if not lifestyle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Lifestyle data not found"
        )

    db.delete(lifestyle)
    db.commit()
    return {"message": "Lifestyle data deleted successfully"}
