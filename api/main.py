from fastapi import FastAPI
from src.schemas import Applicant
from api.predict import score

app = FastAPI(
    title="CreditShield",
    description="Predicts probability of 2-year serious credit delinquency",
    version="1.0"
)

@app.get("/health")
def health():
    """Health check — used by monitoring systems to confirm the app is alive."""
    return {"status": "ok"}

@app.post("/predict")
def predict(applicant: Applicant):
    """
    Score a loan applicant.
    Input: applicant features (validated by Pydantic)
    Output: default probability + risk band
    """
    probability = score(applicant.model_dump())
    return {
        "default_probability": round(probability, 4),
        "risk_band": "high" if probability > 0.5 else "low",
    }