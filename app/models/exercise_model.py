from sqlalchemy import Column, Integer, String

from app.config.database import Base


class Exercise(Base):
    __tablename__ = "exercises"

    exercise_id = Column(Integer, primary_key=True, index=True)
    exercise_name = Column(String(100), nullable=False)
    muscle_group = Column(String(50))
    difficulty = Column(String(20))
    equipment_needed = Column(String(50))
