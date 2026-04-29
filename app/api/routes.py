from fastapi import APIRouter

from app.core.config import get_settings
from app.models.predictor import PredictionRequest, PredictionResponse
from app.services.prediction_service import RuleBasedPredictor

router = APIRouter()
settings = get_settings()
predictor = RuleBasedPredictor(model_version=settings.model_version)


@router.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok", "service": settings.service_name}


@router.post("/predict", response_model=PredictionResponse)
def predict(data: PredictionRequest) -> PredictionResponse:
    return predictor.predict(data)
