import joblib
import shap
import matplotlib.pyplot as plt
from sklearn.calibration import CalibratedClassifierCV, CalibrationDisplay
from src.config import MODELS, REPORTS
from src.data import get_splits

def main():
    X_train, X_test, y_train, y_test = get_splits()

    model = joblib.load(MODELS / "best_model.pkl")
    pre = model.named_steps["pre"]
    clf = model.named_steps["clf"]

    # Transform test data the same way the model preprocesses it
    X_test_transformed = pre.transform(X_test)

    # ── SHAP ──────────────────────────────────────────────────────────────
    print("Computing SHAP values (takes ~1 min)...")
    explainer   = shap.TreeExplainer(clf)
    shap_values = explainer.shap_values(X_test_transformed)

    (REPORTS / "shap_plots").mkdir(parents=True, exist_ok=True)

    # Summary plot — shows feature importance + direction of effect
    shap.summary_plot(shap_values, X_test_transformed,
                      feature_names=list(X_test.columns), show=False)
    plt.tight_layout()
    plt.savefig(REPORTS / "shap_plots" / "shap_summary.png", dpi=150,
                bbox_inches="tight")
    plt.close()
    print("Saved shap_summary.png")

    # Bar plot — simpler view, just mean absolute SHAP per feature
    shap.summary_plot(shap_values, X_test_transformed,
                      feature_names=list(X_test.columns),
                      plot_type="bar", show=False)
    plt.tight_layout()
    plt.savefig(REPORTS / "shap_plots" / "shap_bar.png", dpi=150,
                bbox_inches="tight")
    plt.close()
    print("Saved shap_bar.png")

    # ── Calibration ────────────────────────────────────────────────────────
    from sklearn.frozen import FrozenEstimator
    cal = CalibratedClassifierCV(FrozenEstimator(clf), method="isotonic", cv=5)
    cal.fit(X_test_transformed, y_test)
    fig, ax = plt.subplots()
    CalibrationDisplay.from_estimator(model, X_test, y_test, ax=ax, n_bins=10)
    ax.set_title("Calibration curve")
    fig.savefig(REPORTS / "calibration_curve.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("Saved calibration_curve.png")

if __name__ == "__main__":
    main()