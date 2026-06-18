from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer

def build_preprocessor(numeric_features: list) -> ColumnTransformer:
    """
    Builds a sklearn preprocessing pipeline that:
    1. Fills missing values with the median (handles nulls in MonthlyIncome etc.)
    2. Scales all features to mean=0, std=1 (important for logistic regression)

    ColumnTransformer applies this to the numeric columns only.
    remainder="drop" ignores any columns not in numeric_features.
    """
    numeric = Pipeline([
        ("impute", SimpleImputer(strategy="median")),
        ("scale",  StandardScaler()),
    ])

    return ColumnTransformer(
        transformers=[("num", numeric, numeric_features)],
        remainder="drop"
    )
