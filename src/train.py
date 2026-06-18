import joblib
import mlflow
import mlflow.sklearn
import optuna
import xgboost as xgb
import lightgbm as lgb
from imblearn.pipeline import Pipeline as ImbPipeline   # imblearn's version handles SMOTE
from imblearn.over_sampling import SMOTE
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline

from src.config import EXPERIMENT_NAME, MODELS, REGISTERED_MODEL, SEED
from src.data import get_splits
from src.features import build_preprocessor


def main():
    # ── Load data ──────────────────────────────────────────────────────────
    X_train, X_test, y_train, y_test = get_splits()
    pre = build_preprocessor(list(X_train.columns))

    # Class imbalance ratio: ~14 negatives per positive
    neg = (y_train == 0).sum()
    pos = (y_train == 1).sum()
    spw = neg / pos
    print(f"Class imbalance ratio (neg/pos): {spw:.1f}")

    # Tell MLflow which experiment to log to
    mlflow.set_experiment(EXPERIMENT_NAME)

    best_auc   = 0
    best_model = None

    # ── Run 1: Logistic Regression baseline ────────────────────────────────
    print("\nTraining Run 1: Logistic Regression...")
    with mlflow.start_run(run_name="baseline_logreg"):
        model = Pipeline([
            ("pre", pre),
            ("clf", LogisticRegression(
                max_iter=1000,
                class_weight="balanced",   # handles imbalance
                random_state=SEED
            ))
        ])
        model.fit(X_train, y_train)
        auc = roc_auc_score(y_test, model.predict_proba(X_test)[:, 1])

        # Log to MLflow — these show up in the UI
        mlflow.log_param("model", "logistic_regression")
        mlflow.log_param("class_weight", "balanced")
        mlflow.log_metric("roc_auc", auc)
        mlflow.sklearn.log_model(model, "model", serialization_format="cloudpickle")

        print(f"  ROC-AUC: {auc:.4f}")

    # ── Run 2: XGBoost with scale_pos_weight ───────────────────────────────
    print("\nTraining Run 2: XGBoost...")
    with mlflow.start_run(run_name="xgboost"):
        model = Pipeline([
            ("pre", pre),
            ("clf", xgb.XGBClassifier(
                n_estimators=400,
                max_depth=5,
                learning_rate=0.05,
                scale_pos_weight=spw,      # handles imbalance
                eval_metric="auc",
                random_state=SEED
            ))
        ])
        model.fit(X_train, y_train)
        auc = roc_auc_score(y_test, model.predict_proba(X_test)[:, 1])

        mlflow.log_param("model", "xgboost")
        mlflow.log_param("scale_pos_weight", round(spw, 2))
        mlflow.log_metric("roc_auc", auc)
        mlflow.sklearn.log_model(model, "model", serialization_format="cloudpickle")

        print(f"  ROC-AUC: {auc:.4f}")
        if auc > best_auc:
            best_auc, best_model = auc, model

    # ── Run 3: LightGBM ────────────────────────────────────────────────────
    print("\nTraining Run 3: LightGBM...")
    with mlflow.start_run(run_name="lightgbm"):
        model = Pipeline([
            ("pre", pre),
            ("clf", lgb.LGBMClassifier(
                n_estimators=400,
                max_depth=5,
                learning_rate=0.05,
                is_unbalance=True,         # handles imbalance
                random_state=SEED
            ))
        ])
        model.fit(X_train, y_train)
        auc = roc_auc_score(y_test, model.predict_proba(X_test)[:, 1])

        mlflow.log_param("model", "lightgbm")
        mlflow.log_param("is_unbalance", True)
        mlflow.log_metric("roc_auc", auc)
        mlflow.sklearn.log_model(model, "model", serialization_format="cloudpickle")

        print(f"  ROC-AUC: {auc:.4f}")
        if auc > best_auc:
            best_auc, best_model = auc, model

    # ── Run 4: XGBoost + SMOTE ─────────────────────────────────────────────
    # SMOTE creates synthetic minority class samples before training.
    # We use imblearn's Pipeline (not sklearn's) because it applies
    # SMOTE only during .fit(), not during .transform() — important for
    # avoiding data leakage into the test set.
    print("\nTraining Run 4: XGBoost + SMOTE...")
    with mlflow.start_run(run_name="xgb_smote"):
        model = ImbPipeline([
            ("pre",   pre),
            ("smote", SMOTE(random_state=SEED)),
            ("clf",   xgb.XGBClassifier(
                n_estimators=300,
                eval_metric="auc",
                random_state=SEED
            ))
        ])
        model.fit(X_train, y_train)
        auc = roc_auc_score(y_test, model.predict_proba(X_test)[:, 1])

        mlflow.log_param("model", "xgb_smote")
        mlflow.log_param("sampler", "SMOTE")
        mlflow.log_metric("roc_auc", auc)
        mlflow.sklearn.log_model(model, "model", serialization_format="cloudpickle")

        print(f"  ROC-AUC: {auc:.4f}")
        if auc > best_auc:
            best_auc, best_model = auc, model

    # ── Run 5: Optuna-tuned XGBoost ────────────────────────────────────────
    # Optuna automatically searches for the best hyperparameters.
    # It's smarter than GridSearchCV: instead of trying every combination,
    # it learns which directions are promising and focuses there.
    print("\nTuning Run 5: Optuna XGBoost (30 trials, this takes ~5 min)...")

    def objective(trial):
        params = {
            "max_depth":     trial.suggest_int("max_depth", 3, 8),
            "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.2, log=True),
            "n_estimators":  trial.suggest_int("n_estimators", 200, 600),
            "subsample":     trial.suggest_float("subsample", 0.6, 1.0),
        }
        m = Pipeline([
            ("pre", pre),
            ("clf", xgb.XGBClassifier(
                **params,
                scale_pos_weight=spw,
                eval_metric="auc",
                random_state=SEED
            ))
        ])
        # cross_val_score runs 3-fold CV and returns 3 scores — we average them
        return cross_val_score(m, X_train, y_train,
                               scoring="roc_auc", cv=3, n_jobs=-1).mean()

    optuna.logging.set_verbosity(optuna.logging.WARNING)  # suppress trial noise
    study = optuna.create_study(direction="maximize")
    study.optimize(objective, n_trials=30)

    with mlflow.start_run(run_name="xgb_optuna"):
        model = Pipeline([
            ("pre", pre),
            ("clf", xgb.XGBClassifier(
                **study.best_params,
                scale_pos_weight=spw,
                eval_metric="auc",
                random_state=SEED
            ))
        ])
        model.fit(X_train, y_train)
        auc = roc_auc_score(y_test, model.predict_proba(X_test)[:, 1])

        mlflow.log_params({**study.best_params, "model": "xgb_optuna"})
        mlflow.log_metric("roc_auc", auc)
        mlflow.sklearn.log_model(model, "model", serialization_format="cloudpickle")

        print(f"  ROC-AUC: {auc:.4f}  (best params: {study.best_params})")
        if auc > best_auc:
            best_auc, best_model = auc, model

    # ── Save the best model ────────────────────────────────────────────────
    MODELS.mkdir(exist_ok=True)
    joblib.dump(best_model, MODELS / "best_model.pkl")
    print(f"\nBest model — ROC-AUC {best_auc:.4f} — saved to models/best_model.pkl")


if __name__ == "__main__":
    main()