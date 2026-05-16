from sqlalchemy import Boolean, Column, ForeignKey, Integer

from app.config.database import Base


class Equipment(Base):
    __tablename__ = "equipment"

    equipment_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    gym_access = Column(Boolean, default=False)
    dumbbells = Column(Boolean, default=False)
    resistance_bands = Column(Boolean, default=False)
