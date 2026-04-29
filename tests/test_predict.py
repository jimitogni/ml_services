from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_predict_high_risk() -> None:
    response = client.post(
        "/predict",
        json={"age": 65, "glucose": 140, "hemoglobin": 11.5},
    )

    assert response.status_code == 200
    assert response.json() == {
        "risk_score": 1.0,
        "risk_level": "high",
        "recommendation": "Review required by healthcare professional",
        "model_version": "v0.1-rule-based",
    }


def test_predict_low_risk() -> None:
    response = client.post(
        "/predict",
        json={"age": 35, "glucose": 90},
    )

    assert response.status_code == 200
    assert response.json()["risk_level"] == "low"
    assert response.json()["risk_score"] == 0.0
