from app.models.predictor import PredictionRequest, PredictionResponse, RiskLevel


class RuleBasedPredictor:
    def __init__(self, model_version: str) -> None:
        self.model_version = model_version

    def predict(self, data: PredictionRequest) -> PredictionResponse:
        risk_score = 0.0

        if data.glucose > 125:
            risk_score += 0.6

        if data.age > 60:
            risk_score += 0.3

        if data.hemoglobin is not None and data.hemoglobin < 12:
            risk_score += 0.2

        risk_score = min(risk_score, 1.0)
        risk_level = self._risk_level(risk_score)

        return PredictionResponse(
            risk_score=risk_score,
            risk_level=risk_level,
            recommendation=self._recommendation(risk_level),
            model_version=self.model_version,
        )

    @staticmethod
    def _risk_level(risk_score: float) -> RiskLevel:
        if risk_score >= 0.7:
            return "high"
        if risk_score >= 0.4:
            return "medium"
        return "low"

    @staticmethod
    def _recommendation(risk_level: RiskLevel) -> str:
        if risk_level == "high":
            return "Review required by healthcare professional"
        if risk_level == "medium":
            return "Monitor and review with clinical context"
        return "No immediate risk alert from current rule set"
