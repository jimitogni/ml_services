from typing import Literal

from pydantic import BaseModel, Field

RiskLevel = Literal["low", "medium", "high"]


class PredictionRequest(BaseModel):
    age: int = Field(..., ge=0, le=130)
    glucose: float = Field(..., ge=0)
    hemoglobin: float | None = Field(default=None, ge=0)


class PredictionResponse(BaseModel):
    risk_score: float = Field(..., ge=0, le=1)
    risk_level: RiskLevel
    recommendation: str
    model_version: str
