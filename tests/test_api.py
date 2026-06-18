from fastapi.testclient import TestClient
from api.main import app

# TestClient lets you send HTTP requests to your app without starting a real server
client = TestClient(app)

# A valid sample applicant to reuse across tests
VALID_APPLICANT = {
    "RevolvingUtilizationOfUnsecuredLines": 0.5,
    "age": 35,
    "NumberOfTime30_59DaysPastDueNotWorse": 0,
    "DebtRatio": 0.3,
    "MonthlyIncome": 5000,
    "NumberOfOpenCreditLinesAndLoans": 4,
    "NumberOfTimes90DaysLate": 0,
    "NumberRealEstateLoansOrLines": 1,
    "NumberOfTime60_89DaysPastDueNotWorse": 0,
    "NumberOfDependents": 1,
}

def test_health_returns_200():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_predict_valid_applicant():
    response = client.post("/predict", json=VALID_APPLICANT)
    assert response.status_code == 200
    body = response.json()
    assert 0 <= body["default_probability"] <= 1
    assert body["risk_band"] in ("high", "low")

def test_predict_rejects_underage():
    """age=5 fails the ge=18 Pydantic validator — should return 422."""
    bad = {**VALID_APPLICANT, "age": 5}
    assert client.post("/predict", json=bad).status_code == 422

def test_predict_rejects_missing_field():
    """Missing a required field — should return 422."""
    bad = {k: v for k, v in VALID_APPLICANT.items() if k != "DebtRatio"}
    assert client.post("/predict", json=bad).status_code == 422

def test_predict_high_risk_applicant():
    """Someone with many late payments should score higher risk."""
    risky = {**VALID_APPLICANT, "NumberOfTimes90DaysLate": 10,
             "RevolvingUtilizationOfUnsecuredLines": 0.99}
    response = client.post("/predict", json=risky)
    body = response.json()
    assert body["default_probability"] > 0.1, "High-risk applicant scored too low"