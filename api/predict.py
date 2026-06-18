import joblib
import pandas as pd
from pathlib import Path

# Load the model once when the server starts (not on every request)
MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "best_model.pkl"
_model = None

def _get_model():
    global _model
    if _model is None:
        _model = joblib.load(MODEL_PATH)
    return _model

def score(data: dict) -> float:
    import pandas as pd
    model = _get_model()
    
    # Rename underscore fields to match the column names the model was trained on
    rename = {
        "NumberOfTime30_59DaysPastDueNotWorse": "NumberOfTime30-59DaysPastDueNotWorse",
        "NumberOfTime60_89DaysPastDueNotWorse": "NumberOfTime60-89DaysPastDueNotWorse",
    }
    data = {rename.get(k, k): v for k, v in data.items()}
    
    X = pd.DataFrame([data])
    return float(model.predict_proba(X)[:, 1][0])