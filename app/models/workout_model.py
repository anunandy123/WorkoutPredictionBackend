from sqlalchemy import Column, ForeignKey, Integer, String

from app.config.database import Base


class WorkoutPlan(Base):
    __tablename__ = "workout_plans"

    plan_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    workout_day = Column(String(20))
    exercise_id = Column(Integer, ForeignKey("exercises.exercise_id"))
    sets = Column(Integer)
    reps = Column(Integer)
