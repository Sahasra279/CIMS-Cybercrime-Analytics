# ============================================================
# pages/1_Crime_Analysis.py
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
)
from utils.visualizations import (
    plotly_bar_chart,
    plotly_pie_chart,
    mpl_bar_chart,
    seaborn_heatmap,
)

st.set_page_config(page_title=f"{APP_SHORT_TITLE} | Crime Analysis", page_icon="🔍", layout="wide")

# Load CSS
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
    st.caption("Crime Analysis Module")
    st.markdown("---")

filtered_df, active_filters = render_global_sidebar_filters(incidents_raw, cases_raw)


# ── Page Header ───────────────────────────────────────────────
st.markdown(
    """
    <div class="page-header">
        <h1>🔍 Crime Analysis</h1>
        <p>Detailed breakdown of cybercrime incidents by category, attack channels, geographic distribution, and cross-tabulations.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

render_filter_summary_badge(filtered_df, len(incidents_raw), active_filters)

if filtered_df.empty:
    st.warning("⚠️ No incident records match the selected filter criteria. Please adjust your filters or click 'Clear All Filters' in the sidebar.")
    st.stop()


# ── Row 1: Crime Types & Delivery Channels (2 Columns) ────────
r1_c1, r1_c2 = st.columns(2)

with r1_c1:
    type_counts = filtered_df["incident_type"].value_counts().reset_index()
    type_counts.columns = ["incident_type", "count"]
    fig_type = plotly_bar_chart(
        type_counts,
        x="incident_type",
        y="count",
        title="Incident Volume by Crime Classification",
        color_col="incident_type",
        show_legend=False,
    )
    st.plotly_chart(fig_type, use_container_width=True, config={"responsive": True, "displayModeBar": False})

with r1_c2:
    channel_counts = filtered_df["channel"].value_counts().reset_index()
    channel_counts.columns = ["channel", "count"]
    fig_channel = plotly_pie_chart(
        channel_counts,
        names="channel",
        values="count",
        title="Attack Delivery Channel Distribution",
        hole=0.45,
    )
    st.plotly_chart(fig_channel, use_container_width=True, config={"responsive": True, "displayModeBar": False})

st.markdown("---")


# ── Row 2: Geographic Distribution (2 Columns) ────────────────
st.markdown("### 🗺️ Geographic Distribution")
geo_c1, geo_c2 = st.columns(2)

with geo_c1:
    state_df = filtered_df["state"].value_counts().reset_index()
    state_df.columns = ["state", "count"]
    fig_state = plotly_bar_chart(
        state_df,
        x="state",
        y="count",
        title="Reported Incidents by State",
        color_col="state",
        show_legend=False,
    )
    st.plotly_chart(fig_state, use_container_width=True, config={"responsive": True, "displayModeBar": False})

with geo_c2:
    city_df = filtered_df["city"].value_counts().reset_index()
    city_df.columns = ["city", "count"]
    fig_city = plotly_bar_chart(
        city_df,
        x="city",
        y="count",
        title="Reported Incidents by Metropolitan City",
        color_col="city",
        show_legend=False,
    )
    st.plotly_chart(fig_city, use_container_width=True, config={"responsive": True, "displayModeBar": False})

st.markdown("---")


# ── Row 3: Academic Visualizations (Seaborn & Matplotlib) ─────
st.markdown("### 🎓 Academic Statistical Visualizations (Seaborn & Matplotlib)")
st.caption("Demonstrating Pandas cross-tabulation matrix, Seaborn heatmaps, and Matplotlib static plots.")

stat_c1, stat_c2 = st.columns(2)

with stat_c1:
    st.markdown("#### ⚖️ Priority vs Resolution Status Matrix")
    ct = pd.crosstab(filtered_df["priority"], filtered_df["status"])
    fig_heat = seaborn_heatmap(ct, title="Priority Severity vs Status Cross-Tab", fmt="d", cmap="Blues")
    st.pyplot(fig_heat, use_container_width=True)

with stat_c2:
    st.markdown("#### 📊 Crime Category Distribution (Matplotlib)")
    fig_mpl = mpl_bar_chart(
        labels=type_counts["incident_type"].tolist(),
        values=type_counts["count"].tolist(),
        title="Crime Classification Breakdown",
        xlabel="Incident Category",
        ylabel="Total Cases Logged",
        color=COLORS["accent_blue"],
    )
    st.pyplot(fig_mpl, use_container_width=True)
