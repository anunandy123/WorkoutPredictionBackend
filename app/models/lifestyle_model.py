from sqlalchemy import Column, Float, ForeignKey, Integer

from app.config.database import Base


class Lifestyle(Base):
    __tablename__ = "lifestyle"

    lifestyle_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    sleep_hours = Column(Float)
    stress_level = Column(Integer)
    water_intake = Column(Float)
    sitting_hours = Column(Integer)
