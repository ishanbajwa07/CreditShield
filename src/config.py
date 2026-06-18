from pathlib import Path

# Root of the project 
ROOT = Path(__file__).resolve().parents[1]

# Data Paths
RAW = ROOT / "data" / "raw" / "cs-training.csv"
PROCESSED = ROOT / "data" / "processed" 

# Output Paths
MODELS = ROOT / "models"
REPORTS = ROOT / "reports"

# ML settings
TARGET = "SeriousDlqin2yrs" # The column we're predicting
SEED = 42 # Random seed for reproductibility
EXPERIMENT_NAME  = "creditshield"       # MLflow experiment name
REGISTERED_MODEL = "creditshield_best"  # MLflow model registry name