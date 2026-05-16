from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.config.security import get_current_user
from app.schemas.user_schema import (
    TokenResponse,
    UserLogin,
    UserRegister,
    UserResponse,
    UserUpdate,
)
from app.services.user_service import UserService

router = APIRouter(prefix="/api/users", tags=["users"])


@router.post("/register", response_model=TokenResponse)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """Register a new user."""
    result = UserService.register_user(db, user_data)

    if "error" in result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=result["error"]
        )

    return {
        "access_token": result["access_token"],
        "token_type": result["token_type"],
        "user_id": result["user"]["user_id"],
    }


@router.post("/login", response_model=TokenResponse)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """Login a user."""
    result = UserService.login_user(db, user_data.name, user_data.password)

    if "error" in result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=result["error"]
        )

    return {
        "access_token": result["access_token"],
        "token_type": result["token_type"],
        "user_id": result["user"]["user_id"],
    }


@router.get("/profile", response_model=UserResponse)
def get_profile(
    user_id: int = Depends(get_current_user), db: Session = Depends(get_db)
):
    """Get user profile."""
    result = UserService.get_user_profile(db, user_id)

    if "error" in result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=result["error"]
        )

    return result


@router.put("/profile", response_model=UserResponse)
def update_profile(
    user_data: UserUpdate,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update user profile."""
    result = UserService.update_user_profile(db, user_id, user_data)

    if "error" in result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=result["error"]
        )

    return result


@router.delete("/account")
def delete_account(
    user_id: int = Depends(get_current_user), db: Session = Depends(get_db)
):
    """Delete user account."""
    result = UserService.delete_user_account(db, user_id)

    if "error" in result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=result["error"]
        )

    return result
