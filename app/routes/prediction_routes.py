from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.config.security import get_current_user
from app.repositories.user_repository import UserRepository
from app.schemas.prediction_schema import (
    FitnessPredictionRequest,
    FitnessPredictionRequestPre,
    FitnessPredictionResponse,
    PredictionOptionsResponse,
)
from app.services.prediction_service import PredictionService

router = APIRouter(prefix="/api/predict", tags=["predictions"])


def _handle_prediction(service_call):
    try:
        return service_call()
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc


@router.get("/options", response_model=PredictionOptionsResponse)
def get_prediction_options(_user_id: int = Depends(get_current_user)):
    """Return valid dropdown values loaded from label encoders."""
    return _handle_prediction(PredictionService.get_prediction_options)


@router.post("/", response_model=FitnessPredictionResponse)
def predict_fitness(
    payload: FitnessPredictionRequestPre,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Run the full prediction pipeline across all ML models.

    Automatically includes user's age, weight, and BMI from their profile.
    """
    # Get current user's data
    user = UserRepository.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    # Calculate BMI: weight (kg) / (height (m) ^ 2)
    height_m = user.height / 100  # Convert cm to m
    bmi = user.weight / (height_m**2)

    # Enrich payload with user data
    enriched_payload = payload.model_dump()
    enriched_payload.update(
        {
            "age": user.age,
            "weight_kg": user.weight,
            "gender": user.gender,
            "bmi": round(bmi, 2),
        }
    )
    enriched_payload = FitnessPredictionRequest(**enriched_payload)

    return _handle_prediction(lambda: PredictionService.predict(enriched_payload))
