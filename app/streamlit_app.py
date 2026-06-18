import streamlit as st
import pandas as pd
import numpy as np
import shap
import joblib
import matplotlib.pyplot as plt
from pathlib import Path
from shap.plots import colors as _shap_colors

from styles import get_css

st.set_page_config(page_title="CreditShield", page_icon="🛡️", layout="wide")

if "theme" not in st.session_state:
    st.session_state.theme = "light"
st.markdown(get_css(st.session_state.theme), unsafe_allow_html=True)


@st.cache_resource
def load_model():
    return joblib.load(Path("models/best_model.pkl"))


@st.cache_resource
def get_explainer(_clf):
    return shap.TreeExplainer(_clf)


MODEL = load_model()
PRE   = MODEL.named_steps["pre"]
CLF   = MODEL.named_steps["clf"]

FEATURE_NAMES = [
    "Revolving utilisation", "Age", "30–59 days late", "Debt ratio",
    "Monthly income", "Open credit lines", "90+ days late",
    "Real estate loans", "60–89 days late", "Dependents",
]

SHIELD_SVG = (
    '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" '
    'stroke="var(--accent)" stroke-width="1.8" stroke-linecap="round" '
    'stroke-linejoin="round"><path d="M12 3l7 3v5c0 4.5-3 7.6-7 9'
    '-4-1.4-7-4.5-7-9V6z"/><path d="M9 12l2 2 4-4"/></svg>'
)

CHART_SVG = (
    '<svg width="38" height="38" viewBox="0 0 24 24" fill="none" '
    'stroke="currentColor" stroke-width="1.5" stroke-linecap="round" '
    'stroke-linejoin="round"><line x1="4" y1="20" x2="20" y2="20"/>'
    '<rect x="6" y="12" width="3" height="6"/><rect x="11" y="8" width="3" height="10"/>'
    '<rect x="16" y="4" width="3" height="14"/></svg>'
)


def render_shap_waterfall(sv_row, theme):
    if theme == "dark":
        text_col, muted_col = "#E8EEF6", "#93A1B5"
        pos_col,  neg_col   = "#FB7185", "#60A5FA"
    else:
        text_col, muted_col = "#0F172A", "#64748B"
        pos_col,  neg_col   = "#E11D48", "#2563EB"

    def hx(h):
        h = h.lstrip("#")
        return np.array([int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)])

    _shap_colors.red_rgb  = hx(pos_col)
    _shap_colors.blue_rgb = hx(neg_col)

    plt.rcParams.update({
        "font.family":     "sans-serif",
        "font.sans-serif": ["Inter", "Helvetica Neue", "Arial", "DejaVu Sans"],
        "text.color":      text_col,
        "axes.labelcolor": text_col,
        "xtick.color":     muted_col,
        "ytick.color":     text_col,
        "font.size":       11,
    })

    fig = plt.figure(figsize=(6, 4.2))
    shap.plots.waterfall(sv_row, show=False)
    fig.patch.set_alpha(0.0)
    for ax in fig.axes:
        ax.set_facecolor("none")
        for ln in ax.lines:
            ln.set_color(muted_col)
            ln.set_alpha(0.35)
        for lbl in ax.get_yticklabels():
            lbl.set_color(text_col)
        for lbl in ax.get_xticklabels():
            lbl.set_color(muted_col)
        for spine in ax.spines.values():
            spine.set_visible(False)
    return fig


def section(label):
    st.markdown(f'<div class="cs-section-label">{label}</div>', unsafe_allow_html=True)


head_left, head_right = st.columns([6, 1])
with head_left:
    st.markdown(f"""
        <div class="cs-eyebrow">Explainable credit-risk scoring</div>
        <div class="cs-title"><span class="shield">{SHIELD_SVG}</span>CreditShield</div>
        <div class="cs-tagline">Credit decisions affect millions of people, 
        but the reasoning is rarely explained. This is a machine learning system that predicts loan default risk and tries to change that. One score at a time.</div>
    """, unsafe_allow_html=True)
with head_right:
    if st.button("Light mode" if st.session_state.theme == "dark" else "Dark mode", key="theme_toggle"):
        st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"
        st.rerun()

st.markdown('<div class="cs-rule"></div>', unsafe_allow_html=True)

left, right = st.columns([1.15, 1], gap="large")

with left:
    with st.form("applicant_form", border=False):
        section("Credit behaviour")
        with st.container(border=True):
            c1, c2 = st.columns(2)
            with c1:
                util  = st.slider("Revolving utilisation (% of credit used)", 0.0, 1.0, 0.3,
                                  help="Share of available revolving credit currently in use.")
                lines = st.slider("Open credit lines", 0, 20, 5,
                                  help="Number of open loans and lines of credit.")
            with c2:
                re_loans = st.slider("Real estate loans", 0, 10, 1,
                                     help="Mortgage and home-equity lines of credit.")
                age      = st.slider("Age", 18, 90, 40, help="Applicant age in years.")

        section("Income &amp; obligations")
        with st.container(border=True):
            c3, c4 = st.columns(2)
            with c3:
                income = st.number_input("Monthly income (USD)", 0, 50000, 5000, step=500,
                                         help="Gross monthly income before tax.")
                debt   = st.slider("Debt ratio", 0.0, 1.0, 0.3,
                                   help="Monthly debt payments divided by monthly income.")
            with c4:
                deps = st.number_input("Number of dependents", 0, 10, 1,
                                       help="People financially dependent on the applicant.")

        section("Delinquency history")
        with st.container(border=True):
            c5, c6, c7 = st.columns(3)
            with c5:
                late3059 = st.slider("30–59 days late", 0, 10, 0,
                                     help="Times 30–59 days past due in the last 2 years.")
            with c6:
                late6089 = st.slider("60–89 days late", 0, 10, 0,
                                     help="Times 60–89 days past due in the last 2 years.")
            with c7:
                late90 = st.slider("90+ days late", 0, 10, 0,
                                   help="Times 90+ days past due — a strong default signal.")

        st.markdown('<div style="height:14px"></div>', unsafe_allow_html=True)
        submitted = st.form_submit_button("Score applicant")

with right:
    if submitted:
        row = pd.DataFrame([{
            "RevolvingUtilizationOfUnsecuredLines":   util,
            "age":                                    age,
            "NumberOfTime30-59DaysPastDueNotWorse":   late3059,
            "DebtRatio":                              debt,
            "MonthlyIncome":                          income,
            "NumberOfOpenCreditLinesAndLoans":        lines,
            "NumberOfTimes90DaysLate":                late90,
            "NumberRealEstateLoansOrLines":           re_loans,
            "NumberOfTime60-89DaysPastDueNotWorse":   late6089,
            "NumberOfDependents":                     deps,
        }])

        proba = float(MODEL.predict_proba(row)[:, 1][0])

        if proba >= 0.50:
            band, pill, color = "HIGH RISK", "cs-pill-high", "var(--danger)"
        elif proba >= 0.20:
            band, pill, color = "MODERATE RISK", "cs-pill-med", "var(--warning)"
        else:
            band, pill, color = "LOW RISK", "cs-pill-low", "var(--success)"

        st.markdown(f"""
            <div class="cs-result">
              <div class="cs-prob-label">Default probability</div>
              <div class="cs-prob-value" style="color:{color}">{proba:.1%}</div>
              <span class="cs-pill {pill}">{band}</span>
              <div class="cs-bar-track">
                <div class="cs-bar-fill" style="width:{proba*100:.1f}%; background:{color}"></div>
              </div>
              <div class="cs-bar-caption">Bands · Low &lt;20% · Moderate 20–50% · High ≥50%</div>
            </div>
        """, unsafe_allow_html=True)

        X_t = PRE.transform(row)
        explainer = get_explainer(CLF)
        sv = explainer(X_t)
        sv.feature_names = FEATURE_NAMES

        vals  = np.asarray(sv[0].values).ravel()
        order = np.argsort(np.abs(vals))[::-1][:3]
        st.markdown('<div class="cs-why">What drove this score</div>', unsafe_allow_html=True)
        factors_html = ""
        for i in order:
            up = vals[i] > 0
            factors_html += (
                f'<div class="cs-factor {"up" if up else "down"}">'
                f'<span class="dir">{"▲" if up else "▼"}</span>'
                f'<span class="name">{FEATURE_NAMES[i]}</span>'
                f'<span class="val">{"+" if up else "−"}{abs(vals[i]):.2f}</span>'
                f'</div>'
            )
        st.markdown(factors_html, unsafe_allow_html=True)
        st.markdown(
            '<div class="cs-bar-caption">▲ raises default risk · ▼ lowers it · '
            'values are SHAP contributions to the score.</div>',
            unsafe_allow_html=True,
        )

        st.markdown('<div class="cs-why">Full breakdown</div>', unsafe_allow_html=True)
        fig = render_shap_waterfall(sv[0], st.session_state.theme)
        st.pyplot(fig, bbox_inches="tight")
    else:
        st.markdown(f"""
            <div class="cs-empty">
              <span class="ico">{CHART_SVG}</span>
              Set the applicant's details on the left and select
              <b>Score applicant</b> to generate a default probability
              and a feature-level explanation.
            </div>
        """, unsafe_allow_html=True)

        st.markdown("""
            <div class="cs-method">
              <h4>How this works</h4>
              <div class="cs-method-row"><span class="k">Model</span><span class="v">XGBoost · Optuna-tuned</span></div>
              <div class="cs-method-row"><span class="k">Dataset</span><span class="v">Give Me Some Credit · 150k rows</span></div>
              <div class="cs-method-row"><span class="k">Test ROC-AUC</span><span class="v">0.8699</span></div>
              <div class="cs-method-row"><span class="k">Imbalance handling</span><span class="v">scale_pos_weight · SMOTE</span></div>
              <div class="cs-method-row"><span class="k">Explanations</span><span class="v">SHAP · TreeExplainer</span></div>
            </div>
        """, unsafe_allow_html=True)

st.markdown(
    '<div class="cs-footer">Built by <span class="mono">Ishan</span> · CreditShield · 2026</div>',
    unsafe_allow_html=True,
)