from sqlalchemy.orm import Session

from app.config.security import create_access_token
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserRegister, UserResponse, UserUpdate


class UserService:
    @staticmethod
    def register_user(db: Session, user_data: UserRegister) -> dict:
        """Register a new user."""
        # Check if user already exists
        existing_user = UserRepository.get_user_by_name(db, user_data.name)
        if existing_user:
            return {"error": "User already exists"}

        user = UserRepository.create_user(db, user_data)
        access_token = create_access_token({"sub": user.user_id})

        return {
            "user": UserResponse.from_orm(user).model_dump(),
            "access_token": access_token,
            "token_type": "bearer",
        }

    @staticmethod
    def login_user(db: Session, name: str, password: str) -> dict:
        """Login a user."""
        user = UserRepository.verify_user_password(db, name, password)
        if not user:
            return {"error": "Invalid credentials"}

        access_token = create_access_token({"sub": user.user_id})

        return {
            "user": UserResponse.from_orm(user).model_dump(),
            "access_token": access_token,
            "token_type": "bearer",
        }

    @staticmethod
    def get_user_profile(db: Session, user_id: int) -> dict:
        """Get user profile."""
        user = UserRepository.get_user_by_id(db, user_id)
        if not user:
            return {"error": "User not found"}

        return UserResponse.from_orm(user).model_dump()

    @staticmethod
    def update_user_profile(db: Session, user_id: int, user_data: UserUpdate) -> dict:
        """Update user profile."""
        user = UserRepository.update_user(db, user_id, user_data)
        if not user:
            return {"error": "User not found"}

        return UserResponse.from_orm(user).model_dump()

    @staticmethod
    def delete_user_account(db: Session, user_id: int) -> dict:
        """Delete user account."""
        if UserRepository.delete_user(db, user_id):
            return {"message": "User deleted successfully"}
        return {"error": "User not found"}
