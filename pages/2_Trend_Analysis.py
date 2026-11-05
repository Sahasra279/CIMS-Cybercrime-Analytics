# ============================================================
# pages/2_Trend_Analysis.py
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
    agg_by_month,
)
from utils.visualizations import plotly_line_chart, plotly_bar_chart, mpl_line_chart

st.set_page_config(page_title=f"{APP_SHORT_TITLE} | Trend Analysis", page_icon="📈", layout="wide")

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
    st.caption("Trend Analysis Module")
    st.markdown("---")

df, active_filters = render_global_sidebar_filters(incidents_raw, cases_raw)


# ── Page Header ───────────────────────────────────────────────
st.markdown(
    """
    <div class="page-header">
        <h1>📈 Incident Trend Analysis</h1>
        <p>Temporal trends, moving averages, and monthly cybercrime volume patterns.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

render_filter_summary_badge(df, len(incidents_raw), active_filters)

if df.empty:
    st.warning("⚠️ No incident records match the selected filter criteria. Please adjust your filters or click 'Clear All Filters' in the sidebar.")
    st.stop()


# ── Row 1: Monthly Inflow & Loss Trajectory (2 Columns) ───────
df_monthly = agg_by_month(df)

r1_c1, r1_c2 = st.columns(2)

with r1_c1:
    st.markdown("### 📅 Monthly Incident Volume")
    fig_line = plotly_line_chart(
        df_monthly,
        x="month",
        y="count",
        title="Monthly Incident Volume Trajectory (2024)",
        markers=True,
    )
    st.plotly_chart(fig_line, use_container_width=True, config={"responsive": True, "displayModeBar": False})

with r1_c2:
    st.markdown("### 💰 Monthly Financial Impact Trend")
    fig_fin_trend = plotly_bar_chart(
        df_monthly,
        x="month",
        y="financial_loss",
        title="Reported Financial Losses by Month (INR)",
        color_col="month",
        show_legend=False,
    )
    st.plotly_chart(fig_fin_trend, use_container_width=True, config={"responsive": True, "displayModeBar": False})

st.markdown("---")


# ── Row 2: Monthly Crime Type Pivot ───────────────────────────
st.markdown("### 🔀 Monthly Attack Vector Cross-Tabulation")
temp_df = df.copy()
temp_df["month"] = temp_df["reported_date"].dt.to_period("M").astype(str)
pivot_trend = temp_df.pivot_table(
    index="month",
    columns="incident_type",
    values="incident_id",
    aggfunc="count",
    fill_value=0,
).reset_index()

st.dataframe(pivot_trend, use_container_width=True)

st.markdown("---")


# ── Row 3: Moving Average Smoothing (NumPy & Matplotlib) ──────
st.markdown("### 🌊 Statistical Smoothing & Moving Average (NumPy / Matplotlib)")
st.caption("Demonstrating NumPy numerical operations and rolling window smoothing for second-year B.Tech curriculum.")

df_sorted = df.sort_values("reported_date").copy()
daily_counts = df_sorted.groupby(df_sorted["reported_date"].dt.date).size().reset_index(name="daily_count")
daily_counts["rolling_avg"] = daily_counts["daily_count"].rolling(window=2, min_periods=1).mean()

fig_roll = mpl_line_chart(
    x=[d.strftime("%b %d") for d in daily_counts["reported_date"]],
    y=np.array(daily_counts["rolling_avg"]),
    title="Moving Average Rate (NumPy Smoothed Window)",
    xlabel="Incident Date",
    ylabel="Average Daily Volume",
    color=COLORS["accent_cyan"],
)
st.pyplot(fig_roll, use_container_width=True)
