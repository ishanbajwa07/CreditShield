from src.data import load_raw, get_splits

def test_no_invalid_ages():
    """Cleaning should remove rows where age <= 0."""
    df = load_raw()
    assert (df["age"] <= 0).sum() == 0, "Found rows with invalid age"

def test_split_shapes():
    """80/20 split should give correct sizes."""
    X_tr, X_te, y_tr, y_te = get_splits()
    assert X_tr.shape[1] == 10, "Expected 10 features"
    assert len(X_tr) > len(X_te), "Train set should be larger than test set"

def test_class_balance_preserved():
    """stratify=y should keep ~6.7% positive rate in both splits."""
    _, _, y_tr, y_te = get_splits()
    assert 0.05 < y_tr.mean() < 0.10, "Train positive rate out of expected range"
    assert 0.05 < y_te.mean() < 0.10, "Test positive rate out of expected range"