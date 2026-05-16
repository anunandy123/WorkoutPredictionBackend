from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.config.security import get_current_user
from app.models.equipment_model import Equipment
from app.schemas.equipment_schema import (
    EquipmentCreate,
    EquipmentResponse,
    EquipmentUpdate,
)

router = APIRouter(prefix="/api/equipment", tags=["equipment"])


@router.post("/", response_model=EquipmentResponse)
def create_equipment(
    equipment_data: EquipmentCreate,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create equipment entry for user."""
    db_equipment = Equipment(
        user_id=user_id,
        gym_access=equipment_data.gym_access,
        dumbbells=equipment_data.dumbbells,
        resistance_bands=equipment_data.resistance_bands,
    )
    db.add(db_equipment)
    db.commit()
    db.refresh(db_equipment)
    return db_equipment


@router.get("/", response_model=EquipmentResponse)
def get_equipment(
    user_id: int = Depends(get_current_user), db: Session = Depends(get_db)
):
    """Get user's equipment information."""
    equipment = db.query(Equipment).filter(Equipment.user_id == user_id).first()
    if not equipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Equipment not found"
        )
    return equipment


@router.put("/", response_model=EquipmentResponse)
def update_equipment(
    equipment_data: EquipmentUpdate,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update user's equipment information."""
    equipment = db.query(Equipment).filter(Equipment.user_id == user_id).first()
    if not equipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Equipment not found"
        )

    update_data = equipment_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(equipment, key, value)

    db.commit()
    db.refresh(equipment)
    return equipment


@router.delete("/")
def delete_equipment(
    user_id: int = Depends(get_current_user), db: Session = Depends(get_db)
):
    """Delete user's equipment information."""
    equipment = db.query(Equipment).filter(Equipment.user_id == user_id).first()
    if not equipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Equipment not found"
        )

    db.delete(equipment)
    db.commit()
    return {"message": "Equipment deleted successfully"}
