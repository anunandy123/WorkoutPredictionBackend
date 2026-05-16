from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    Numeric,
    String,
)

from app.config.database import Base


class FoodLog(Base):
    __tablename__ = "food_logs"

    food_log_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    food_name = Column(String(100))
    calories = Column(Integer)
    protein = Column(Integer)
    logged_at = Column(DateTime, default=datetime.utcnow)


class Calories(Base):
    __tablename__ = "calories"

    food_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    asked_by_user_id = Column(Integer, ForeignKey("users.user_id"))
    fitness_goal = Column(String(100))
    calories = Column(Numeric(10, 3))
    proteins = Column(Numeric(10, 3))
    fat = Column(Numeric(10, 3))
    carbs = Column(Numeric(10, 3))
    food_group = Column(String(30))
