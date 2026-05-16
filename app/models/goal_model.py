from sqlalchemy import Column, ForeignKey, Integer, String

from app.config.database import Base


class Goal(Base):
    __tablename__ = "goals"

    goal_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    fitness_goal = Column(String(100))
    target_weight = Column(Integer)
    workout_days = Column(Integer)
    workout_minutes = Column(Integer)
