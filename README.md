# Clinic ML Service

FastAPI service for machine learning inference, OCR experiments, and AI-assisted clinical risk alerts.

This repository is intended to run separately from the main clinic backend. The backend should call this service over HTTP instead of running heavy ML work directly.

## Architecture

```text
User / Browser
  -> Frontend - Next.js
  -> Backend API - FastAPI
  -> ML Service - FastAPI / Python model API
  -> Model files / OCR / prediction logic
```

Typical flow:

1. The backend receives exam data or an exam image.
2. The backend saves the original file or structured data.
3. The backend calls this ML service.
4. The ML service returns extracted values or a prediction.
5. The backend saves the reviewed result in PostgreSQL.

For healthcare workflows, OCR and prediction output should be reviewed by a healthcare professional before becoming official patient data.

## Project Structure

```text
clinic-ml-service/
  app/
    main.py
    api/
      routes.py
    models/
      predictor.py
    services/
      ocr_service.py
      prediction_service.py
    core/
      config.py
  tests/
    test_health.py
    test_predict.py
  models/
    README.md
  requirements.txt
  Dockerfile
  docker-compose.yml
  docker-compose.prod.yml
  .github/
    workflows/
      ci.yml
```

## Run Locally

Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

Start the API on port `8001`:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

Health check:

```bash
curl http://localhost:8001/health
```

Prediction example:

```bash
curl -X POST http://localhost:8001/predict \
  -H "Content-Type: application/json" \
  -d '{"age": 65, "glucose": 140, "hemoglobin": 11.5}'
```

Expected response:

```json
{
  "risk_score": 1.0,
  "risk_level": "high",
  "recommendation": "Review required by healthcare professional",
  "model_version": "v0.1-rule-based"
}
```

## Run With Docker

```bash
docker compose up --build
```

The service will be available at:

```text
http://localhost:8001
```

## Pull Published Image

After a successful push to `main`, GitHub Actions publishes the image to GitHub Container Registry:

```text
ghcr.io/jimitogni/ml_services:latest
```

Branch pushes also get branch tags, for example:

```text
ghcr.io/jimitogni/ml_services:dev
ghcr.io/jimitogni/ml_services:main
```

On a server, pull and run the published image with:

```bash
docker pull ghcr.io/jimitogni/ml_services:latest
docker compose -f docker-compose.prod.yml up -d
```

If the package is private, log in first:

```bash
echo YOUR_TOKEN | docker login ghcr.io -u jimitogni --password-stdin
```

## API Endpoints

`GET /health`

Returns service health information.

`POST /predict`

Runs the first rule-based risk predictor. This is not a final medical model. It exists to prove the service architecture before replacing the rules with a trained model.

Request body:

```json
{
  "age": 65,
  "glucose": 140,
  "hemoglobin": 11.5
}
```

## Backend Integration Example

When this service runs in the same Docker network as the backend, the backend can call it by service name:

```python
import httpx

ML_SERVICE_URL = "http://ml-service:8001"


async def call_prediction_service(payload: dict):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{ML_SERVICE_URL}/predict", json=payload)
        response.raise_for_status()
        return response.json()
```

## Tests

```bash
pytest
```

## CI/CD

GitHub Actions runs on pushes and pull requests to `main` and `dev`.

The pipeline:

1. Installs Python dependencies.
2. Runs `pytest`.
3. Builds the Docker image.
4. Pushes the Docker image to GitHub Container Registry on `push` events.

Pull requests build the image but do not publish it.

## Roadmap

1. Keep `/health` and `/predict` stable.
2. Train a first simple model with Logistic Regression, Random Forest, or XGBoost.
3. Save the model with `joblib` and load it from the API.
4. Add `POST /extract-exam-data` for OCR.
5. Add model versioning with MLflow, DVC, S3, or MinIO.
6. Add automated home lab deployment.
7. Add Jenkins after the GitHub Actions flow is working.
