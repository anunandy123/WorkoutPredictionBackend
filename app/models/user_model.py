from sqlalchemy import Column, Float, Integer, String

from app.config.database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer)
    gender = Column(String(20))
    height = Column(Float)
    weight = Column(Float)
    fitness_level = Column(String(50))
    password = Column(String(255))
