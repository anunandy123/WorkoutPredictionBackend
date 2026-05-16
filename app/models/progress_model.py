from datetime import date

from sqlalchemy import Boolean, Column, Date, Float, ForeignKey, Integer

from app.config.database import Base


class DailyProgress(Base):
    __tablename__ = "daily_progress"

    progress_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    weight = Column(Float)
    calories_consumed = Column(Integer)
    workout_completed = Column(Boolean, default=False)
    energy_level = Column(Integer)
    tracked_on = Column(Date, default=date.today)
