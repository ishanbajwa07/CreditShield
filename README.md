<<<<<<< HEAD
**[Live demo →](https://ishanbajwa07-creditshield.hf.space)**<img width="1352" height="878" alt="Screenshot 2026-06-19 at 10 11 38 am" src="https://github.com/user-attachments/assets/67498991-c6ee-4c7c-97be-c6a93ef512b0" />

=======
**[Live demo →](https://ishanbajwa07-creditshield.hf.space)**
>>>>>>> 59e5caa6c2e43f356e2a38bf952650a602aacf06
![CI](https://github.com/ishanbajwa07/CreditShield/actions/workflows/ci.yml/badge.svg)

# CreditShield

Credit decisions affect millions of people, but the reasoning behind them is rarely explained. CreditShield predicts the probability that a loan applicant becomes seriously delinquent within two years, and shows the factors behind every score.

It's a full MLOps project rather than just a model in a notebook: train → track → explain → serve → containerise → test → monitor → deploy.

**Stack:** scikit-learn · XGBoost · LightGBM · Optuna · SHAP · MLflow · FastAPI · Docker · pytest · GitHub Actions · Evidently · Streamlit

---

## The app

Enter an applicant's details and the model returns a default probability, a risk band (Low <20% / Moderate 20–50% / High ≥50%), and a per-applicant SHAP breakdown of what pushed the score up or down.

![CreditShield light mode](reports/screenshots/app_light.png)

![CreditShield scored, dark mode](reports/screenshots/app_dark_scored.png)

---

## Results

Five models tracked in MLflow, sorted by test ROC-AUC. The Optuna-tuned XGBoost is the one that ships.

| Model | ROC-AUC | Notes |
|---|---|---|
| Logistic regression (baseline) | 0.8000 | class_weight="balanced" |
| XGBoost | 0.8668 | scale_pos_weight=14 |
| LightGBM | 0.8674 | is_unbalance=True |
| XGBoost + SMOTE | 0.8386 | imbalanced-learn oversampling |
| **XGBoost + Optuna (best)** | **0.8699** | deployed model |

![MLflow runs](reports/screenshots/mlflow_runs.png)

---

## SHAP — top default drivers

![SHAP summary](reports/shap_plots/shap_summary.png)

`RevolvingUtilizationOfUnsecuredLines` and `NumberOfTimes90DaysLate` dominate. Being maxed out on available credit and having a recent serious delinquency are the two strongest signals of future default — which lines up with how a human underwriter would think about it.

---

## API

The model is also served as a FastAPI endpoint with Pydantic-validated input. `/health` for a liveness check, `/predict` for scoring.

![FastAPI predict response](reports/screenshots/fastapi_predict.png)

---

## A few decisions worth explaining

**Handling the imbalance.** The dataset is only ~6.7% positive, so a model that always predicts "no default" already scores 93% accuracy while catching zero actual defaults. I used `scale_pos_weight` (and `is_unbalance` for LightGBM) to penalise missed defaults in proportion to how rare they are.

**SMOTE vs class-weighting.** These are two different ways to attack the same imbalance problem, so instead of guessing which is better I ran both as separate MLflow experiments and compared. Class-weighting won here.

**Calibration.** Raw XGBoost probabilities are overconfident. For a credit decision the actual number matters — a "0.80" should mean default happens roughly 80% of the time — so I ran isotonic calibration to correct it.

**Optuna over grid search.** Optuna uses a Bayesian (TPE) search that concentrates trials where the results are promising, so 30 trials found better hyperparameters than a much larger grid would have.

---

## Run locally

```bash
git clone https://github.com/ishanbajwa07/CreditShield
cd CreditShield
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
# drop cs-training.csv into data/raw/ first
python -m src.train
python -m src.explain
uvicorn api.main:app --reload
```

## Run with Docker

```bash
docker build -t creditshield .
docker run -p 8000:8000 creditshield
curl http://localhost:8000/health
```

## Run the Streamlit demo

```bash
streamlit run app/streamlit_app.py
```

---

## What I'd add next

<<<<<<< HEAD
- Automatic retraining trigger when Evidently flags data drift
- A `/batch` endpoint for scoring many applicants in one request
- Monitoring actual model performance over time, not just input drift
=======
- Retraining trigger when Evidently flags drift
- A /batch endpoint for scoring multiple applicants at once
- Model performance monitoring (not just data drift)
>>>>>>> 59e5caa6c2e43f356e2a38bf952650a602aacf06
