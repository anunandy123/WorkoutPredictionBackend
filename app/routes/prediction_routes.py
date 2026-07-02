from fastapi import APIRouter, Depends, HTTPException, status

from app.config.security import get_current_user
from app.schemas.prediction_schema import (
    CaloriePredictionRequest,
    CaloriePredictionResponse,
    DietPredictionRequest,
    DietPredictionResponse,
    ExercisePredictionRequest,
    ExercisePredictionResponse,
    FitnessPredictionRequest,
    FitnessPredictionResponse,
    MealPredictionRequest,
    MealPredictionResponse,
    PredictionOptionsResponse,
    WorkoutPredictionRequest,
    WorkoutPredictionResponse,
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


@router.post("/calories", response_model=CaloriePredictionResponse)
def predict_calories(
    payload: CaloriePredictionRequest,
    _user_id: int = Depends(get_current_user),
):
    """Predict calories burned using linear regression and scaler models."""
    return _handle_prediction(
        lambda: PredictionService.predict_calories(payload)
    )


@router.post("/workout", response_model=WorkoutPredictionResponse)
def predict_workout(
    payload: WorkoutPredictionRequest,
    _user_id: int = Depends(get_current_user),
):
    """Recommend workout type using the workout random forest model."""
    return _handle_prediction(lambda: PredictionService.predict_workout(payload))


@router.post("/diet", response_model=DietPredictionResponse)
def predict_diet(
    payload: DietPredictionRequest,
    _user_id: int = Depends(get_current_user),
):
    """Recommend diet type using the diet random forest model."""
    return _handle_prediction(lambda: PredictionService.predict_diet(payload))


@router.post("/exercise", response_model=ExercisePredictionResponse)
def predict_exercise(
    payload: ExercisePredictionRequest,
    _user_id: int = Depends(get_current_user),
):
    """Recommend exercise using the exercise random forest model."""
    return _handle_prediction(
        lambda: PredictionService.predict_exercise(payload)
    )


@router.post("/meal", response_model=MealPredictionResponse)
def predict_meal(
    payload: MealPredictionRequest,
    _user_id: int = Depends(get_current_user),
):
    """Recommend meal type using the meal decision tree model."""
    return _handle_prediction(lambda: PredictionService.predict_meal(payload))


@router.post("/", response_model=FitnessPredictionResponse)
def predict_fitness(
    payload: FitnessPredictionRequest,
    _user_id: int = Depends(get_current_user),
):
    """Run the full prediction pipeline across all ML models."""
    return _handle_prediction(lambda: PredictionService.predict(payload))
