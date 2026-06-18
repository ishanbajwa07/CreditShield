import numpy as np
import pandas as pd
from evidently import Report
from evidently.presets import DataDriftPreset
from src.config import REPORTS, SEED
from src.data import get_splits


def main():
    X_train, X_test, *_ = get_splits()

    # Simulate drift: inflate MonthlyIncome in the "current" batch
    rng = np.random.default_rng(SEED)
    current = X_test.copy()
    current["MonthlyIncome"] = current["MonthlyIncome"] * rng.uniform(2, 3, size=len(current))
    print("Simulated drift: MonthlyIncome artificially inflated 2-3x")

    report = Report(metrics=[DataDriftPreset()])
    my_eval = report.run(reference_data=X_train, current_data=current)

    out = REPORTS / "drift"
    out.mkdir(parents=True, exist_ok=True)

    my_eval.save_html(str(out / "drift_report.html"))
    print("Drift report saved → reports/drift/drift_report.html")


if __name__ == "__main__":
    main()