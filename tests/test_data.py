import pandas as pd
import numpy as np
from src.data import load_raw, get_splits
from src.config import RAW

def make_synthetic():
    """Create a tiny synthetic dataset matching the real schema for CI testing."""
    np.random.seed(42)
    n = 1000
    df = pd.DataFrame({
        "SeriousDlqin2yrs":                       np.random.binomial(1, 0.067, n),
        "RevolvingUtilizationOfUnsecuredLines":    np.random.uniform(0, 1, n),
        "age":                                     np.random.randint(18, 80, n),
        "NumberOfTime30-59DaysPastDueNotWorse":    np.random.randint(0, 5, n),
        "DebtRatio":                               np.random.uniform(0, 1, n),
        "MonthlyIncome":                           np.random.uniform(1000, 10000, n),
        "NumberOfOpenCreditLinesAndLoans":         np.random.randint(0, 15, n),
        "NumberOfTimes90DaysLate":                 np.random.randint(0, 5, n),
        "NumberRealEstateLoansOrLines":            np.random.randint(0, 5, n),
        "NumberOfTime60-89DaysPastDueNotWorse":    np.random.randint(0, 5, n),
        "NumberOfDependents":                      np.random.randint(0, 5, n),
    })
    # Add one bad age row to test cleaning
    df.iloc[0, df.columns.get_loc("age")] = 0
    return df

def test_no_invalid_ages(tmp_path, monkeypatch):
    """Cleaning should remove rows where age <= 0."""
    csv = tmp_path / "cs-training.csv"
    make_synthetic().to_csv(csv)
    monkeypatch.setattr("src.data.RAW", csv)
    df = load_raw()
    assert (df["age"] <= 0).sum() == 0

def test_split_shapes(tmp_path, monkeypatch):
    """80/20 split should give correct sizes."""
    csv = tmp_path / "cs-training.csv"
    make_synthetic().to_csv(csv)
    monkeypatch.setattr("src.data.RAW", csv)
    X_tr, X_te, y_tr, y_te = get_splits()
    assert X_tr.shape[1] == 10
    assert len(X_tr) > len(X_te)

def test_class_balance_preserved(tmp_path, monkeypatch):
    """stratify=y should keep positive rate in both splits."""
    csv = tmp_path / "cs-training.csv"
    make_synthetic().to_csv(csv)
    monkeypatch.setattr("src.data.RAW", csv)
    _, _, y_tr, y_te = get_splits()
    assert 0.01 < y_tr.mean() < 0.20
    assert 0.01 < y_te.mean() < 0.20