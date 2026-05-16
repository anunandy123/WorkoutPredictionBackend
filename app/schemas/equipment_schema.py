from typing import Optional

from pydantic import BaseModel


class EquipmentCreate(BaseModel):
    gym_access: bool = False
    dumbbells: bool = False
    resistance_bands: bool = False


class EquipmentUpdate(BaseModel):
    gym_access: Optional[bool] = None
    dumbbells: Optional[bool] = None
    resistance_bands: Optional[bool] = None


class EquipmentResponse(BaseModel):
    equipment_id: int
    user_id: int
    gym_access: bool
    dumbbells: bool
    resistance_bands: bool

    class Config:
        from_attributes = True
