from sqlalchemy.orm import Session

from app.config.security import hash_password, verify_password
from app.models.user_model import User
from app.schemas.user_schema import UserRegister, UserUpdate


class UserRepository:
    @staticmethod
    def create_user(db: Session, user_data: UserRegister) -> User:
        """Create a new user."""
        hashed_password = hash_password(user_data.password)
        db_user = User(
            name=user_data.name,
            password=hashed_password,
            age=user_data.age,
            gender=user_data.gender,
            height=user_data.height,
            weight=user_data.weight,
            fitness_level=user_data.fitness_level,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> User:
        """Get user by ID."""
        return db.query(User).filter(User.user_id == user_id).first()

    @staticmethod
    def get_user_by_name(db: Session, name: str) -> User:
        """Get user by name."""
        return db.query(User).filter(User.name == name).first()

    @staticmethod
    def update_user(db: Session, user_id: int, user_data: UserUpdate) -> User:
        """Update user information."""
        db_user = UserRepository.get_user_by_id(db, user_id)
        if db_user:
            update_data = user_data.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_user, key, value)
            db.commit()
            db.refresh(db_user)
        return db_user

    @staticmethod
    def delete_user(db: Session, user_id: int) -> bool:
        """Delete user by ID."""
        db_user = UserRepository.get_user_by_id(db, user_id)
        if db_user:
            db.delete(db_user)
            db.commit()
            return True
        return False

    @staticmethod
    def verify_user_password(db: Session, name: str, password: str) -> User:
        """Verify user credentials."""
        user = UserRepository.get_user_by_name(db, name)
        if user and verify_password(password, user.password):
            return user
        return None
