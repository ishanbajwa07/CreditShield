from src.data import get_splits
from src.features import build_preprocessor

def test_preprocessor_shape():
    """Preprocessor should output same number of columns as input."""
    X_tr, X_te, *_ = get_splits()
    pre = build_preprocessor(list(X_tr.columns))
    pre.fit(X_tr)
    out = pre.transform(X_te)
    assert out.shape == (len(X_te), X_tr.shape[1])

def test_preprocessor_no_nulls():
    """After imputation, there should be no missing values."""
    import numpy as np
    X_tr, X_te, *_ = get_splits()
    pre = build_preprocessor(list(X_tr.columns))
    pre.fit(X_tr)
    out = pre.transform(X_te)
    assert not np.isnan(out).any(), "Preprocessor left NaN values"