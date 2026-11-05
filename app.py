# ============================================================
# app.py — CIMS Executive Analytics Dashboard
# Cybercrime Incident Management System (CIMS)
# Cybercrime Analytics & Visualization System
# ============================================================

import sys
import os

# Make sibling packages importable
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
import pandas as pd
import numpy as np

from config import (
    APP_TITLE,
    APP_SHORT_TITLE,
    APP_ICON,
    APP_VERSION,
    PAGE_LAYOUT,
    SIDEBAR_STATE,
)
from utils.data_processing import (
    load_all_datasets,
    render_global_sidebar_filters,
    render_filter_summary_badge,
    compute_cims_kpis,
    agg_by_type,
    agg_by_status,
    agg_by_priority,
    agg_by_month,
    agg_cases_by_status,
    agg_evidence_by_status,
)
from utils.visualizations import (
    plotly_bar_chart,
    plotly_pie_chart,
    plotly_line_chart,
    plotly_loss_bar,
)


# ── Page configuration ────────────────────────────────────────
st.set_page_config(
    page_title=f"{APP_SHORT_TITLE} | Dashboard",
    page_icon=APP_ICON,
    layout=PAGE_LAYOUT,
    initial_sidebar_state=SIDEBAR_STATE,
)


# ── Load custom CSS ───────────────────────────────────────────
def load_css(css_path: str) -> None:
    """Inject local CSS file."""
    css_file = os.path.join(os.path.dirname(__file__), css_path)
    if os.path.exists(css_file):
        with open(css_file, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css("assets/styles.css")


# ── Data Ingestion ────────────────────────────────────────────
datasets = load_all_datasets()
incidents_raw = datasets["incidents"]
cases_raw = datasets["cases"]
evidence_raw = datasets["evidence"]
users_raw = datasets["users"]
audit_logs_raw = datasets["audit_logs"]


# ── Render Global Sidebar Filters (Consistent across all pages) ──
with st.sidebar:
    st.markdown(f"## {APP_ICON} {APP_SHORT_TITLE}")
    st.caption(f"**{APP_VERSION}**")
    st.markdown("---")

filtered_incidents, active_filters = render_global_sidebar_filters(incidents_raw, cases_raw)


# ── Compute Dynamic KPIs based on filtered data ───────────────
kpis = compute_cims_kpis(filtered_incidents, cases_raw, evidence_raw)


# ── Header Banner ─────────────────────────────────────────────
st.markdown(
    f"""
    <div class="page-header">
        <h1>{APP_ICON} {APP_TITLE}</h1>
        <p>Real-time incident intelligence, investigation tracking, and financial impact analytics powered by CIMS CSV dataset.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Active Filter Summary Banner ──────────────────────────────
render_filter_summary_badge(filtered_incidents, len(incidents_raw), active_filters)


# ── KPI Metric Cards (5 responsive cards) ─────────────────────
st.markdown("### 📊 Key Performance Indicators")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        label="🗂️ Total Incidents",
        value=f"{kpis['total_incidents']:,}",
        delta=f"{len(incidents_raw)} in dataset",
        delta_color="off",
    )

with col2:
    st.metric(
        label="💼 Total Cases",
        value=f"{kpis['total_cases']:,}",
        delta="Linked cases",
        delta_color="off",
    )

with col3:
    st.metric(
        label="⏳ Active Cases",
        value=f"{kpis['open_cases']:,}",
        delta="Under Investigation",
        delta_color="inverse",
    )

with col4:
    st.metric(
        label="✅ Resolved Cases",
        value=f"{kpis['resolved_cases']:,}",
        delta="Closed / Settled",
        delta_color="normal",
    )

with col5:
    st.metric(
        label="💰 Financial Loss",
        value=f"₹{kpis['total_loss_inr']:,.0f}",
        delta=f"Avg: ₹{kpis['avg_loss_inr']:,.0f}",
        delta_color="off",
    )

st.markdown("---")


# ── Check if filtered data is empty ───────────────────────────
if filtered_incidents.empty:
    st.warning("⚠️ No incident records match the current filter selection. Please adjust your filters or click 'Clear All Filters' in the sidebar.")
    st.stop()


# ── Row 1: Crime Distribution & Status Breakdown (2 Columns) ──
st.markdown("### 🔍 Incident Classification & Case Pipeline")
r1_c1, r1_c2 = st.columns(2)

with r1_c1:
    df_types = agg_by_type(filtered_incidents)
    fig_types = plotly_bar_chart(
        df_types,
        x="incident_type",
        y="count",
        title="Incidents by Crime Classification",
        color_col="incident_type",
        show_legend=False,
    )
    st.plotly_chart(fig_types, use_container_width=True, config={"responsive": True, "displayModeBar": False})

with r1_c2:
    df_statuses = agg_by_status(filtered_incidents)
    fig_status = plotly_pie_chart(
        df_statuses,
        names="status",
        values="count",
        title="Incidents by Resolution Status",
        hole=0.45,
    )
    st.plotly_chart(fig_status, use_container_width=True, config={"responsive": True, "displayModeBar": False})


# ── Row 2: Priority Spectrum & Timeline Trends (2 Columns) ────
st.markdown("### 📈 Severity Spread & Monthly Inflow Trends")
r2_c1, r2_c2 = st.columns(2)

with r2_c1:
    df_priorities = agg_by_priority(filtered_incidents)
    fig_priority = plotly_bar_chart(
        df_priorities,
        x="priority",
        y="count",
        title="Incidents by Priority Severity Level",
        color_col="priority",
        show_legend=False,
    )
    st.plotly_chart(fig_priority, use_container_width=True, config={"responsive": True, "displayModeBar": False})

with r2_c2:
    df_monthly = agg_by_month(filtered_incidents)
    fig_trend = plotly_line_chart(
        df_monthly,
        x="month",
        y="count",
        title="Monthly Incident Inflow Trajectory",
    )
    st.plotly_chart(fig_trend, use_container_width=True, config={"responsive": True, "displayModeBar": False})


# ── Row 3: Financial Losses & Investigation Status (2 Columns) ─
st.markdown("### 💰 Financial Exposure & Evidence Pipeline")
r3_c1, r3_c2 = st.columns(2)

with r3_c1:
    fig_loss = plotly_loss_bar(
        df_types,
        x="incident_type",
        y="total_loss",
        title="Total Financial Loss by Attack Vector (INR)",
    )
    st.plotly_chart(fig_loss, use_container_width=True, config={"responsive": True, "displayModeBar": False})

with r3_c2:
    linked_case_ids = filtered_incidents["case_id"].dropna().unique().tolist()
    df_cases_status = agg_cases_by_status(cases_raw, linked_case_ids)
    fig_cases = plotly_pie_chart(
        df_cases_status,
        names="case_status",
        values="count",
        title="Active Investigation Cases by Status",
        hole=0.4,
    )
    st.plotly_chart(fig_cases, use_container_width=True, config={"responsive": True, "displayModeBar": False})

st.markdown("---")


# ── Filtered Incidents Summary Table ──────────────────────────
with st.expander("📋 View Active Filtered Records", expanded=False):
    st.dataframe(
        filtered_incidents[[
            "incident_id", "reported_date", "incident_type", "channel",
            "city", "state", "financial_loss_inr", "priority", "status", "case_id"
        ]],
        use_container_width=True,
    )
    st.caption(f"Displaying {len(filtered_incidents)} of {len(incidents_raw)} total incident records.")

st.markdown(
    "<p style='text-align:center; color:#64748b; font-size:0.8rem;'>"
    f"{APP_ICON} {APP_TITLE} · {APP_VERSION} · Pure CSV Architecture · No External Database Required"
    "</p>",
    unsafe_allow_html=True,
)
