import pandas as pd
from sklearn.model_selection import train_test_split
from src.config import RAW, TARGET, SEED

def load_raw() -> pd.DataFrame:
    """Load the CSV and apply basic cleaning."""
    df = pd.read_csv(RAW, index_col=0)

    # Drop impossible ages (data quality issue in the original dataset)
    before = len(df)
    df = df[df["age"] > 0]
    print(f"Dropped {before - len(df)} rows with age <= 0")

    return df

def get_splits():

    '''Returns: X_train, X_test, y_train, y_test'''
    df = load_raw()
    X = df.drop(columns=[TARGET])
    y = df[TARGET]

    return train_test_split(
        X, y,
        test_size=0.2,       # 80% train, 20% test
        stratify=y,          # preserve class balance in both splits
        random_state=SEED
    )