import streamlit as st
import pandas as pd
import shap
import joblib
import matplotlib.pyplot as plt
from pathlib import Path

# Load model once
MODEL = joblib.load(Path("models/best_model.pkl"))
PRE   = MODEL.named_steps["pre"]
CLF   = MODEL.named_steps["clf"]

st.set_page_config(page_title="CreditShield", page_icon="🛡️")
st.title("🛡️ CreditShield — Loan Default Risk Scorer")
st.caption("Enter applicant details to predict 2-year default probability.")

with st.form("applicant_form"):
    col1, col2 = st.columns(2)

    with col1:
        age      = st.slider("Age", 18, 90, 40)
        util     = st.slider("Revolving utilisation (% of credit used)", 0.0, 1.0, 0.3)
        debt     = st.slider("Debt ratio", 0.0, 1.0, 0.3)
        income   = st.number_input("Monthly income (USD)", 0, 50000, 5000, step=500)
        deps     = st.number_input("Number of dependents", 0, 10, 1)

    with col2:
        late90   = st.slider("Times 90+ days late (last 2 yrs)", 0, 10, 0)
        late6089 = st.slider("Times 60–89 days late", 0, 10, 0)
        late3059 = st.slider("Times 30–59 days late", 0, 10, 0)
        lines    = st.slider("Open credit lines", 0, 20, 5)
        re_loans = st.slider("Real estate loans", 0, 10, 1)

    submitted = st.form_submit_button("Score applicant")

if submitted:
    row = pd.DataFrame([{
        "RevolvingUtilizationOfUnsecuredLines":   util,
        "age":                                    age,
        "NumberOfTime30-59DaysPastDueNotWorse":   late3059,
        "DebtRatio":                              debt,
        "MonthlyIncome":                          income,
        "NumberOfOpenCreditLinesAndLoans":        lines,
        "NumberOfTimes90DaysLate":                late90,
        "NumberRealEstateLoansOrLines":            re_loans,
        "NumberOfTime60-89DaysPastDueNotWorse":   late6089,
        "NumberOfDependents":                     deps,
    }])

    proba = float(MODEL.predict_proba(row)[:, 1][0])
    band  = "HIGH RISK" if proba > 0.5 else "LOW RISK"

    st.divider()
    col_a, col_b = st.columns(2)
    col_a.metric("Default probability", f"{proba:.1%}")
    color = "red" if proba > 0.5 else "green"
    col_b.markdown(f"### :{color}[{band}]")

    # Per-applicant SHAP waterfall — shows which features drove THIS prediction
    st.subheader("Why this score?")
    X_t = PRE.transform(row)
    exp = shap.TreeExplainer(CLF)
    sv  = exp(X_t)
    fig, ax = plt.subplots()
    sv.feature_names = [
        "RevolvingUtilization", "age", "30-59DaysLate", "DebtRatio",
        "MonthlyIncome", "OpenCreditLines", "90DaysLate",
        "RealEstateLoans", "60-89DaysLate", "Dependents"
    ]
    shap.plots.waterfall(sv[0], show=False)
    st.pyplot(fig, bbox_inches="tight")