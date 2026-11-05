# ============================================================
# pages/3_Financial_Analysis.py
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
)
from utils.visualizations import (
    plotly_loss_bar,
    plotly_treemap,
    seaborn_boxplot,
)

st.set_page_config(page_title=f"{APP_SHORT_TITLE} | Financial Analysis", page_icon="💰", layout="wide")

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
    st.caption("Financial Analysis Module")
    st.markdown("---")

df, active_filters = render_global_sidebar_filters(incidents_raw, cases_raw)


# ── Page Header ───────────────────────────────────────────────
st.markdown(
    """
    <div class="page-header">
        <h1>💰 Financial Impact Analysis</h1>
        <p>Quantitative monetary damage evaluation, loss distributions, high-impact cases, and NumPy statistical measures.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

render_filter_summary_badge(df, len(incidents_raw), active_filters)

if df.empty:
    st.warning("⚠️ No incident records match the selected filter criteria. Please adjust your filters or click 'Clear All Filters' in the sidebar.")
    st.stop()


# ── Financial KPI Metrics (4 responsive cards) ────────────────
f_col1, f_col2, f_col3, f_col4 = st.columns(4)
total_loss = df["financial_loss_inr"].sum()
avg_loss = df["financial_loss_inr"].mean() if len(df) else 0.0
max_loss = df["financial_loss_inr"].max() if len(df) else 0.0
num_impacted = (df["financial_loss_inr"] > 0).sum()

with f_col1:
    st.metric("Total Cumulative Loss", f"₹{total_loss:,.0f}")
with f_col2:
    st.metric("Mean Loss per Case", f"₹{avg_loss:,.0f}")
with f_col3:
    st.metric("Peak Loss Record", f"₹{max_loss:,.0f}")
with f_col4:
    st.metric("Impacted Cases", f"{num_impacted} of {len(df)}")

st.markdown("---")


# ── Row 1: Loss by Category & Treemap (2 Columns) ─────────────
r1_c1, r1_c2 = st.columns(2)

with r1_c1:
    loss_by_type = (
        df.groupby("incident_type", as_index=False)
        .agg(total_loss=("financial_loss_inr", "sum"), count=("incident_id", "count"))
        .sort_values("total_loss", ascending=False)
    )
    fig_bar = plotly_loss_bar(
        loss_by_type,
        x="incident_type",
        y="total_loss",
        title="Aggregate Financial Loss by Crime Vector (INR)",
    )
    st.plotly_chart(fig_bar, use_container_width=True, config={"responsive": True, "displayModeBar": False})

with r1_c2:
    fig_tree = plotly_treemap(
        df,
        path_cols=["state", "incident_type"],
        values_col="financial_loss_inr",
        title="Hierarchical Loss Proportion: State → Threat Vector",
    )
    st.plotly_chart(fig_tree, use_container_width=True, config={"responsive": True, "displayModeBar": False})

st.markdown("---")


# ── Row 2: Top High-Impact Cybercrime Cases ───────────────────
st.markdown("### 🏆 Top High-Value Cybercrime Incidents")
top_incidents = (
    df.sort_values("financial_loss_inr", ascending=False)
    [["incident_id", "incident_type", "city", "state", "priority", "status", "financial_loss_inr"]]
    .head(8)
    .copy()
)
top_incidents["financial_loss_inr"] = top_incidents["financial_loss_inr"].apply(lambda v: f"₹{v:,.2f}")
st.dataframe(top_incidents, use_container_width=True)

st.markdown("---")


# ── Row 3: Academic Visualizations (NumPy & Seaborn) ──────────
st.markdown("### 🎓 Academic Statistical Dispersion (NumPy & Seaborn)")
r3_col1, r3_col2 = st.columns(2)

with r3_col1:
    st.markdown("#### 📦 Loss Variance & Outlier Distribution (Seaborn)")
    fig_box = seaborn_boxplot(
        df=df,
        x="priority",
        y="financial_loss_inr",
        title="Financial Loss Dispersion by Priority Severity Level",
    )
    st.pyplot(fig_box, use_container_width=True)

with r3_col2:
    st.markdown("#### 🔢 NumPy Parametric & Non-Parametric Measures")
    np_stats = compute_numpy_stats(df["financial_loss_inr"])
    
    stats_df = pd.DataFrame([
        {"Metric": "Sample Size (N)", "Value": f"{np_stats['count']}"},
        {"Metric": "Arithmetic Mean", "Value": f"₹{np_stats['mean']:,.2f}"},
        {"Metric": "Median (50th %ile)", "Value": f"₹{np_stats['median']:,.2f}"},
        {"Metric": "Standard Deviation", "Value": f"₹{np_stats['std']:,.2f}"},
        {"Metric": "25th Percentile (Q1)", "Value": f"₹{np_stats['q25']:,.2f}"},
        {"Metric": "75th Percentile (Q3)", "Value": f"₹{np_stats['q75']:,.2f}"},
        {"Metric": "Interquartile Range (IQR)", "Value": f"₹{np_stats['iqr']:,.2f}"},
        {"Metric": "Maximum Loss", "Value": f"₹{np_stats['max']:,.2f}"},
    ])
    st.dataframe(stats_df, hide_index=True, use_container_width=True)
