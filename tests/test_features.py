import numpy as np
from tests.test_data import make_synthetic
from src.features import build_preprocessor
from src.data import get_splits
from sklearn.model_selection import train_test_split
from src.config import TARGET, SEED

def test_preprocessor_shape(tmp_path, monkeypatch):
    csv = tmp_path / "cs-training.csv"
    make_synthetic().to_csv(csv)
    monkeypatch.setattr("src.data.RAW", csv)
    X_tr, X_te, *_ = get_splits()
    pre = build_preprocessor(list(X_tr.columns))
    pre.fit(X_tr)
    out = pre.transform(X_te)
    assert out.shape == (len(X_te), X_tr.shape[1])

def test_preprocessor_no_nulls(tmp_path, monkeypatch):
    csv = tmp_path / "cs-training.csv"
    make_synthetic().to_csv(csv)
    monkeypatch.setattr("src.data.RAW", csv)
    X_tr, X_te, *_ = get_splits()
    pre = build_preprocessor(list(X_tr.columns))
    pre.fit(X_tr)
    out = pre.transform(X_te)
    assert not np.isnan(out).any()