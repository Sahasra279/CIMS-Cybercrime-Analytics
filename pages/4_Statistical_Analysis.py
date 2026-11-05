# ============================================================
# pages/4_Statistical_Analysis.py
# Cybercrime Incident Management System (CIMS)
# Cybercrime Analytics & Visualization System
# ============================================================

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
import pandas as pd
import numpy as np

from config import APP_ICON, APP_SHORT_TITLE, COLORS
from utils.data_processing import (
    load_all_datasets,
    render_global_sidebar_filters,
    render_filter_summary_badge,
    compute_numpy_stats,
    normalise_series,
)
from utils.visualizations import (
    seaborn_heatmap,
    seaborn_histogram,
    plotly_scatter_chart,
)

st.set_page_config(page_title=f"{APP_SHORT_TITLE} | Statistical Analysis", page_icon="📊", layout="wide")

css_path = os.path.join(os.path.dirname(__file__), "..", "assets", "styles.css")
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ── Load Data & Global Shared Sidebar Filters ─────────────────
datasets = load_all_datasets()
incidents_raw = datasets["incidents"]
cases_raw = datasets["cases"]

with st.sidebar:
    st.markdown(f"## {APP_ICON} {APP_SHORT_TITLE}")
    st.caption("Statistical Analysis Module")
    st.markdown("---")

incidents, active_filters = render_global_sidebar_filters(incidents_raw, cases_raw)


# ── Page Header ───────────────────────────────────────────────
st.markdown(
    """
    <div class="page-header">
        <h1>📊 Statistical Analysis & Data Science</h1>
        <p>Correlation matrices, probability density distributions, and explicit NumPy mathematical operations.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

render_filter_summary_badge(incidents, len(incidents_raw), active_filters)

if incidents.empty:
    st.warning("⚠️ No incident records match the selected filter criteria. Please adjust your filters or click 'Clear All Filters' in the sidebar.")
    st.stop()


# ── Feature Engineering for Correlation ───────────────────────
analysis_df = incidents.copy()

priority_map = {"Low": 1, "Medium": 2, "High": 3, "Critical": 4}
status_map = {"Reported": 1, "Pending": 2, "Under Investigation": 3, "Resolved": 4}

analysis_df["priority_num"] = analysis_df["priority"].map(priority_map).fillna(1)
analysis_df["status_num"] = analysis_df["status"].map(status_map).fillna(1)
analysis_df["normalized_loss"] = normalise_series(analysis_df["financial_loss_inr"])
analysis_df["report_month"] = analysis_df["reported_date"].dt.month.fillna(1)


# ── Row 1: Seaborn Heatmap & Histogram (2 Columns) ────────────
r1_c1, r1_c2 = st.columns(2)

with r1_c1:
    st.markdown("### 🌡️ Pearson Correlation Heatmap (Seaborn)")
    numeric_cols = analysis_df[["financial_loss_inr", "priority_num", "status_num", "report_month", "normalized_loss"]]
    corr_matrix = numeric_cols.corr()
    fig_corr = seaborn_heatmap(
        corr_matrix,
        title="Incident Metric Pearson Correlation Matrix",
        fmt=".2f",
        cmap="coolwarm",
    )
    st.pyplot(fig_corr, use_container_width=True)

with r1_c2:
    st.markdown("### 📉 Probability Density & KDE (Seaborn)")
    fig_hist = seaborn_histogram(
        series=analysis_df["financial_loss_inr"],
        bins=10,
        title="Financial Loss Probability Density Curve",
        xlabel="Financial Loss in INR (₹)",
        color=COLORS["accent_purple"],
    )
    st.pyplot(fig_hist, use_container_width=True)

st.markdown("---")


# ── Row 2: NumPy Mathematical Operations & Normalisation ──────
st.markdown("### 🔢 Explicit NumPy Array & Matrix Operations")
st.caption("Demonstrating array slicing, standard deviations, and min-max scaling for academic presentation.")

num_c1, num_c2 = st.columns(2)

with num_c1:
    loss_array = np.array(analysis_df["financial_loss_inr"].values, dtype=float)
    st.markdown("#### NumPy Vector Summary")
    st.code(
        f"""# NumPy Vector Operations on Incident Loss
loss_vector = np.array(N={len(loss_array)})

Mean:       np.mean()        = ₹{np.mean(loss_array):,.2f}
Variance:   np.var()         = {np.var(loss_array):,.2f}
Std Dev:    np.std()         = ₹{np.std(loss_array):,.2f}
Median:     np.median()      = ₹{np.median(loss_array):,.2f}
25th %ile:  np.percentile()  = ₹{np.percentile(loss_array, 25):,.2f}
75th %ile:  np.percentile()  = ₹{np.percentile(loss_array, 75):,.2f}
IQR:        Q3 - Q1          = ₹{np.percentile(loss_array, 75) - np.percentile(loss_array, 25):,.2f}
        """,
        language="python",
    )

with num_c2:
    st.markdown("#### Min-Max Normalised Feature Space")
    st.caption("Formula: \\(X_{norm} = \\frac{X - X_{min}}{X_{max} - X_{min}}\\)")
    norm_preview = analysis_df[["incident_id", "incident_type", "financial_loss_inr", "normalized_loss"]].head(6)
    st.dataframe(norm_preview, use_container_width=True)

st.markdown("---")


# ── Row 3: Interactive Plotly Scatter ─────────────────────────
st.markdown("### 🔵 Multi-dimensional Feature Scatter (Plotly)")
fig_scatter = plotly_scatter_chart(
    analysis_df,
    x="priority",
    y="financial_loss_inr",
    color_col="incident_type",
    size_col="priority_num",
    title="Priority Severity vs Financial Loss Impact",
)
st.plotly_chart(fig_scatter, use_container_width=True, config={"responsive": True, "displayModeBar": False})
