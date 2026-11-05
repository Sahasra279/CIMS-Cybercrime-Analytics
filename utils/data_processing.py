# ============================================================
# utils/data_processing.py
# Cybercrime Incident Management System (CIMS)
# Cybercrime Analytics & Visualization System
# ============================================================
# Handles loading, caching, shared global filtering, search,
# persistent editing, and statistical aggregation of the
# 5 CIMS CSV datasets.
# ============================================================

import os
import numpy as np
import pandas as pd
from datetime import datetime, date
import streamlit as st

from config import (
    INCIDENTS_CSV,
    CASES_CSV,
    EVIDENCE_CSV,
    USERS_CSV,
    AUDIT_LOGS_CSV,
    PRIORITY_LEVELS,
)

# ============================================================
# 1. Dataset Schemas (fallback definitions if CSV is missing)
# ============================================================

INCIDENT_COLUMNS = [
    "incident_id", "reported_date", "incident_type", "channel",
    "city", "state", "financial_loss_inr", "priority", "status",
    "assigned_user_id", "case_id"
]

CASE_COLUMNS = [
    "case_id", "incident_id", "case_title", "case_status",
    "assigned_user_id", "created_date", "closed_date"
]

EVIDENCE_COLUMNS = [
    "evidence_id", "case_id", "evidence_description", "evidence_type",
    "collected_date", "collected_by_user_id", "verification_status"
]

USER_COLUMNS = [
    "user_id", "full_name", "role", "email", "account_status"
]

AUDIT_LOG_COLUMNS = [
    "log_id", "user_id", "record_reference", "action", "timestamp"
]


# ============================================================
# 2. CSV Loaders with graceful fallback
# ============================================================

def safe_read_csv(filepath: str, expected_cols: list) -> pd.DataFrame:
    """
    Safely read a CSV file into a Pandas DataFrame.
    If the file is missing or corrupted, returns an empty DataFrame
    with the expected columns.
    """
    if not os.path.exists(filepath):
        return pd.DataFrame(columns=expected_cols)
    try:
        df = pd.read_csv(filepath)
        for col in expected_cols:
            if col not in df.columns:
                df[col] = None
        return df[expected_cols]
    except Exception as e:
        st.warning(f"Warning: Could not read {os.path.basename(filepath)}: {e}")
        return pd.DataFrame(columns=expected_cols)


def load_all_datasets():
    """
    Load all five CIMS CSV datasets.
    Ensures datetime types and numeric types are properly converted.
    """
    incidents = safe_read_csv(INCIDENTS_CSV, INCIDENT_COLUMNS)
    cases = safe_read_csv(CASES_CSV, CASE_COLUMNS)
    evidence = safe_read_csv(EVIDENCE_CSV, EVIDENCE_COLUMNS)
    users = safe_read_csv(USERS_CSV, USER_COLUMNS)
    audit_logs = safe_read_csv(AUDIT_LOGS_CSV, AUDIT_LOG_COLUMNS)

    # Type conversions
    if not incidents.empty:
        incidents["reported_date"] = pd.to_datetime(incidents["reported_date"], errors="coerce")
        incidents["financial_loss_inr"] = pd.to_numeric(incidents["financial_loss_inr"], errors="coerce").fillna(0.0)

    if not cases.empty:
        cases["created_date"] = pd.to_datetime(cases["created_date"], errors="coerce")
        cases["closed_date"] = pd.to_datetime(cases["closed_date"], errors="coerce")

    if not evidence.empty:
        evidence["collected_date"] = pd.to_datetime(evidence["collected_date"], errors="coerce")

    if not audit_logs.empty:
        audit_logs["timestamp"] = pd.to_datetime(audit_logs["timestamp"], errors="coerce")

    return {
        "incidents": incidents,
        "cases": cases,
        "evidence": evidence,
        "users": users,
        "audit_logs": audit_logs,
    }


def save_dataset(dataset_name: str, df: pd.DataFrame) -> bool:
    """
    Persist changes back to the corresponding CSV file.
    """
    file_map = {
        "incidents": INCIDENTS_CSV,
        "cases": CASES_CSV,
        "evidence": EVIDENCE_CSV,
        "users": USERS_CSV,
        "audit_logs": AUDIT_LOGS_CSV,
    }
    if dataset_name not in file_map:
        return False
    
    filepath = file_map[dataset_name]
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        save_df = df.copy()
        if "reported_date" in save_df.columns:
            save_df["reported_date"] = pd.to_datetime(save_df["reported_date"]).dt.strftime("%Y-%m-%d")
        if "created_date" in save_df.columns:
            save_df["created_date"] = pd.to_datetime(save_df["created_date"]).dt.strftime("%Y-%m-%d")
        if "closed_date" in save_df.columns:
            save_df["closed_date"] = pd.to_datetime(save_df["closed_date"]).dt.strftime("%Y-%m-%d")
        if "collected_date" in save_df.columns:
            save_df["collected_date"] = pd.to_datetime(save_df["collected_date"]).dt.strftime("%Y-%m-%d")
        if "timestamp" in save_df.columns:
            save_df["timestamp"] = pd.to_datetime(save_df["timestamp"]).dt.strftime("%Y-%m-%d %H:%M:%S")

        save_df.to_csv(filepath, index=False)
        return True
    except Exception as e:
        st.error(f"Error saving {dataset_name}: {e}")
        return False


def update_record(dataset_name: str, id_col: str, record_id: str, updated_fields: dict) -> bool:
    """
    Update fields for a specific record identified by id_col == record_id.
    Persists changes back to the corresponding CSV file.
    """
    datasets = load_all_datasets()
    if dataset_name not in datasets:
        return False
    df = datasets[dataset_name]
    idx = df[df[id_col].astype(str) == str(record_id)].index
    if idx.empty:
        return False
    
    for col, val in updated_fields.items():
        if col in df.columns:
            df.loc[idx, col] = val
            
    return save_dataset(dataset_name, df)


def delete_record(dataset_name: str, id_col: str, record_id: str) -> bool:
    """
    Remove a specific record identified by id_col == record_id.
    Persists changes back to the corresponding CSV file.
    """
    datasets = load_all_datasets()
    if dataset_name not in datasets:
        return False
    df = datasets[dataset_name]
    initial_len = len(df)
    df = df[df[id_col].astype(str) != str(record_id)].copy()
    if len(df) == initial_len:
        return False
        
    return save_dataset(dataset_name, df)


def log_audit_action(user_id: str, record_ref: str, action: str):
    """
    Add a new entry to audit_logs.csv persistently.
    """
    try:
        logs_df = safe_read_csv(AUDIT_LOGS_CSV, AUDIT_LOG_COLUMNS)
        next_id = f"LOG-{len(logs_df) + 501}"
        new_row = pd.DataFrame([{
            "log_id": next_id,
            "user_id": user_id,
            "record_reference": record_ref,
            "action": action,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }])
        updated_logs = pd.concat([logs_df, new_row], ignore_index=True)
        save_dataset("audit_logs", updated_logs)
    except Exception:
        pass


# ============================================================
# 3. Merging & Shared Global Filtering
# ============================================================

def get_merged_incidents_cases(incidents_df: pd.DataFrame, cases_df: pd.DataFrame) -> pd.DataFrame:
    """
    Enrich incidents DataFrame with case_status and case_title.
    """
    if incidents_df.empty:
        return incidents_df.copy()
    
    if cases_df.empty:
        df = incidents_df.copy()
        df["case_status"] = "Unassigned"
        df["case_title"] = "None"
        return df

    cases_sub = cases_df[["case_id", "case_title", "case_status"]].drop_duplicates("case_id")
    merged = incidents_df.merge(cases_sub, on="case_id", how="left")
    merged["case_status"] = merged["case_status"].fillna("Unassigned")
    merged["case_title"] = merged["case_title"].fillna("None")
    return merged


def apply_cims_filters(
    incidents_df: pd.DataFrame,
    cases_df: pd.DataFrame,
    date_range: tuple | list | None = None,
    incident_type: str | list | None = None,
    status: str | list | None = None,
    priority: str | list | None = None,
    location: str | list | None = None,
) -> pd.DataFrame:
    """
    Apply programmatic multi-attribute filters across incidents merged with cases.
    Supports both single-string values and list selections.
    """
    df = get_merged_incidents_cases(incidents_df, cases_df)
    if df.empty:
        return df

    # Date range
    if date_range and len(date_range) == 2 and date_range[0] and date_range[1]:
        start_d, end_d = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
        df = df[(df["reported_date"] >= start_d) & (df["reported_date"] <= end_d)]

    # Incident type
    if incident_type:
        if isinstance(incident_type, list):
            df = df[df["incident_type"].isin(incident_type)]
        elif incident_type != "All":
            df = df[df["incident_type"] == incident_type]

    # Status
    if status:
        if isinstance(status, list):
            df = df[df["status"].isin(status)]
        elif status != "All":
            df = df[df["status"] == status]

    # Priority
    if priority:
        if isinstance(priority, list):
            df = df[df["priority"].isin(priority)]
        elif priority != "All":
            df = df[df["priority"] == priority]

    # Location (matches state or city)
    if location:
        if isinstance(location, list):
            df = df[df["state"].isin(location) | df["city"].isin(location)]
        elif location != "All":
            df = df[(df["state"] == location) | (df["city"] == location)]

    return df


def _reset_filters(min_d, max_d):
    """Callback to reset all session_state filter keys to defaults."""
    st.session_state["f_date_range"] = (min_d, max_d)
    st.session_state["f_incident_type"] = "All"
    st.session_state["f_status"] = "All"
    st.session_state["f_priority"] = "All"
    st.session_state["f_location"] = "All"


def render_global_sidebar_filters(
    incidents_df: pd.DataFrame,
    cases_df: pd.DataFrame,
) -> tuple[pd.DataFrame, dict]:
    """
    Renders a unified, clearly visible filter panel in the sidebar.
    Maintains persistent filter state across all pages via st.session_state.

    Includes:
    - 📅 Date range filter
    - 🏷️ Crime/Incident Type dropdown
    - 📌 Incident Status dropdown
    - ⚡ Priority dropdown
    - 📍 State/Location dropdown
    - 🔄 Clear All Filters button

    Returns:
    --------
    (filtered_incidents_df, active_filters_dict)
    """
    # Determine date bounds
    if not incidents_df.empty and "reported_date" in incidents_df.columns and incidents_df["reported_date"].notna().any():
        min_date = incidents_df["reported_date"].dropna().min().date()
        max_date = incidents_df["reported_date"].dropna().max().date()
    else:
        min_date = date(2024, 1, 1)
        max_date = date.today()

    # Initialize session state keys if not already present
    if "f_date_range" not in st.session_state or not st.session_state["f_date_range"]:
        st.session_state["f_date_range"] = (min_date, max_date)
    if "f_incident_type" not in st.session_state:
        st.session_state["f_incident_type"] = "All"
    if "f_status" not in st.session_state:
        st.session_state["f_status"] = "All"
    if "f_priority" not in st.session_state:
        st.session_state["f_priority"] = "All"
    if "f_location" not in st.session_state:
        st.session_state["f_location"] = "All"

    # Prepare dropdown option lists
    all_types = ["All"] + sorted(incidents_df["incident_type"].dropna().unique().tolist()) if not incidents_df.empty else ["All"]
    all_statuses = ["All"] + sorted(incidents_df["status"].dropna().unique().tolist()) if not incidents_df.empty else ["All"]
    all_priorities = ["All", "Critical", "High", "Medium", "Low"]
    all_locations = ["All"] + sorted(incidents_df["state"].dropna().unique().tolist()) if not incidents_df.empty else ["All"]

    # Render Sidebar Filter Controls
    with st.sidebar:
        st.markdown("### 🎛️ Dashboard Filters")
        
        # 1. Date Range Filter
        date_val = st.date_input(
            "📅 Date Range",
            value=st.session_state["f_date_range"],
            min_value=min_date,
            max_value=max_date,
            key="f_date_range",
            help="Filter data by reported date range",
        )

        # 2. Incident Type Dropdown
        idx_type = all_types.index(st.session_state["f_incident_type"]) if st.session_state["f_incident_type"] in all_types else 0
        sel_type = st.selectbox(
            "🏷️ Incident Type",
            options=all_types,
            index=idx_type,
            key="f_incident_type",
        )

        # 3. Incident Status Dropdown
        idx_status = all_statuses.index(st.session_state["f_status"]) if st.session_state["f_status"] in all_statuses else 0
        sel_status = st.selectbox(
            "📌 Incident Status",
            options=all_statuses,
            index=idx_status,
            key="f_status",
        )

        # 4. Priority Dropdown
        idx_prio = all_priorities.index(st.session_state["f_priority"]) if st.session_state["f_priority"] in all_priorities else 0
        sel_priority = st.selectbox(
            "⚡ Priority Level",
            options=all_priorities,
            index=idx_prio,
            key="f_priority",
        )

        # 5. State / Location Dropdown
        idx_loc = all_locations.index(st.session_state["f_location"]) if st.session_state["f_location"] in all_locations else 0
        sel_location = st.selectbox(
            "📍 State / Location",
            options=all_locations,
            index=idx_loc,
            key="f_location",
        )

        # 6. Clear All Filters Button
        st.button(
            "🔄 Clear All Filters",
            on_click=_reset_filters,
            args=(min_date, max_date),
            use_container_width=True,
            help="Reset all filters back to default (view all data)",
        )

        st.markdown("---")
        st.markdown(
            f"<div style='font-size:0.75rem; color:#64748b; line-height:1.4;'>"
            f"<b>Active Filters:</b><br>"
            f"• Type: <code>{sel_type}</code><br>"
            f"• Status: <code>{sel_status}</code><br>"
            f"• Priority: <code>{sel_priority}</code><br>"
            f"• Location: <code>{sel_location}</code>"
            f"</div>",
            unsafe_allow_html=True,
        )

    # Apply filters using Pandas
    df = get_merged_incidents_cases(incidents_df, cases_df)
    if not df.empty:
        # Date filter
        if isinstance(date_val, (tuple, list)) and len(date_val) == 2 and date_val[0] and date_val[1]:
            start_d, end_d = pd.to_datetime(date_val[0]), pd.to_datetime(date_val[1])
            df = df[(df["reported_date"] >= start_d) & (df["reported_date"] <= end_d)]

        # Type filter
        if sel_type and sel_type != "All":
            df = df[df["incident_type"] == sel_type]

        # Status filter
        if sel_status and sel_status != "All":
            df = df[df["status"] == sel_status]

        # Priority filter
        if sel_priority and sel_priority != "All":
            df = df[df["priority"] == sel_priority]

        # Location filter (matches state or city)
        if sel_location and sel_location != "All":
            df = df[(df["state"] == sel_location) | (df["city"] == sel_location)]

    active_filters = {
        "date_range": date_val,
        "incident_type": sel_type,
        "status": sel_status,
        "priority": sel_priority,
        "location": sel_location,
        "is_filtered": (
            sel_type != "All" or
            sel_status != "All" or
            sel_priority != "All" or
            sel_location != "All" or
            (isinstance(date_val, (tuple, list)) and len(date_val) == 2 and (date_val[0] != min_date or date_val[1] != max_date))
        ),
    }

    return df, active_filters


def render_filter_summary_badge(filtered_df: pd.DataFrame, total_count: int, active_filters: dict):
    """
    Renders a clean status banner showing active filters and matching record count.
    """
    if active_filters.get("is_filtered", False):
        st.markdown(
            f"""
            <div class="filter-active-pill">
                <span>🔍 Filtered View: <strong>{len(filtered_df)} of {total_count}</strong> incidents match criteria</span>
                <span style="color:#64748b;">(Type: <b>{active_filters['incident_type']}</b> | Status: <b>{active_filters['status']}</b> | Priority: <b>{active_filters['priority']}</b> | Loc: <b>{active_filters['location']}</b>)</span>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ============================================================
# 4. Search Functionality (for Dataset Explorer)
# ============================================================

def search_dataframe(df: pd.DataFrame, search_query: str, search_cols: list | None = None) -> pd.DataFrame:
    """
    Filter DataFrame rows where any text column contains the search query.
    Case-insensitive search across incident_id, case_id, type, status, location, etc.
    """
    if df.empty or not search_query or not search_query.strip():
        return df.copy()

    query = search_query.strip()
    cols = search_cols if search_cols else df.columns.tolist()

    # Build mask across all relevant text-searchable columns
    mask = pd.Series(False, index=df.index)
    for col in cols:
        if col in df.columns:
            mask = mask | df[col].astype(str).str.contains(query, case=False, na=False)

    return df[mask].copy()


# ============================================================
# 5. Summary Statistics & KPI Calculations
# ============================================================

def compute_cims_kpis(filtered_incidents: pd.DataFrame, cases_df: pd.DataFrame, evidence_df: pd.DataFrame) -> dict:
    """
    Compute core CIMS KPIs based on filtered incidents and linked cases/evidence.
    """
    total_incidents = len(filtered_incidents)
    total_loss = float(filtered_incidents["financial_loss_inr"].sum()) if total_incidents else 0.0

    # Linked cases
    linked_case_ids = filtered_incidents["case_id"].dropna().unique() if not filtered_incidents.empty else []
    relevant_cases = cases_df[cases_df["case_id"].isin(linked_case_ids)] if not cases_df.empty else pd.DataFrame()

    total_cases = len(relevant_cases)
    open_cases = len(relevant_cases[relevant_cases["case_status"].isin(["Open", "Under Investigation"])]) if total_cases else 0
    resolved_cases = len(relevant_cases[relevant_cases["case_status"].isin(["Closed", "Resolved"])]) if total_cases else 0

    # Linked evidence
    relevant_evidence = evidence_df[evidence_df["case_id"].isin(linked_case_ids)] if not evidence_df.empty else pd.DataFrame()
    verified_evidence = len(relevant_evidence[relevant_evidence["verification_status"] == "Verified"]) if not relevant_evidence.empty else 0

    return {
        "total_incidents": total_incidents,
        "total_cases": total_cases,
        "open_cases": open_cases,
        "resolved_cases": resolved_cases,
        "total_loss_inr": total_loss,
        "avg_loss_inr": (total_loss / total_incidents) if total_incidents else 0.0,
        "verified_evidence": verified_evidence,
        "total_evidence": len(relevant_evidence),
    }


# ============================================================
# 6. Aggregation Helpers for Charts
# ============================================================

def agg_by_type(df: pd.DataFrame) -> pd.DataFrame:
    """Incident count and total financial loss by incident type."""
    if df.empty:
        return pd.DataFrame(columns=["incident_type", "count", "total_loss"])
    return (
        df.groupby("incident_type", as_index=False)
        .agg(count=("incident_id", "count"), total_loss=("financial_loss_inr", "sum"))
        .sort_values("count", ascending=False)
    )


def agg_by_status(df: pd.DataFrame) -> pd.DataFrame:
    """Incident count by status."""
    if df.empty:
        return pd.DataFrame(columns=["status", "count"])
    return (
        df.groupby("status", as_index=False)
        .agg(count=("incident_id", "count"))
        .sort_values("count", ascending=False)
    )


def agg_by_priority(df: pd.DataFrame) -> pd.DataFrame:
    """Incident count by priority level."""
    if df.empty:
        return pd.DataFrame(columns=["priority", "count"])
    order = {"Critical": 4, "High": 3, "Medium": 2, "Low": 1}
    agg = df.groupby("priority", as_index=False).agg(count=("incident_id", "count"))
    agg["order"] = agg["priority"].map(order).fillna(0)
    return agg.sort_values("order", ascending=False).drop(columns=["order"])


def agg_by_month(df: pd.DataFrame) -> pd.DataFrame:
    """Monthly incident trend."""
    if df.empty or "reported_date" not in df.columns:
        return pd.DataFrame(columns=["month", "count", "financial_loss"])
    
    temp = df.copy()
    temp["month"] = temp["reported_date"].dt.to_period("M").astype(str)
    return (
        temp.groupby("month", as_index=False)
        .agg(count=("incident_id", "count"), financial_loss=("financial_loss_inr", "sum"))
        .sort_values("month")
    )


def agg_cases_by_status(cases_df: pd.DataFrame, linked_case_ids: list | None = None) -> pd.DataFrame:
    """Case count by case_status."""
    if cases_df.empty:
        return pd.DataFrame(columns=["case_status", "count"])
    cdf = cases_df if linked_case_ids is None else cases_df[cases_df["case_id"].isin(linked_case_ids)]
    return (
        cdf.groupby("case_status", as_index=False)
        .agg(count=("case_id", "count"))
        .sort_values("count", ascending=False)
    )


def agg_evidence_by_status(evidence_df: pd.DataFrame, linked_case_ids: list | None = None) -> pd.DataFrame:
    """Evidence count by verification status."""
    if evidence_df.empty:
        return pd.DataFrame(columns=["verification_status", "count"])
    edf = evidence_df if linked_case_ids is None else evidence_df[evidence_df["case_id"].isin(linked_case_ids)]
    return (
        edf.groupby("verification_status", as_index=False)
        .agg(count=("evidence_id", "count"))
        .sort_values("count", ascending=False)
    )


# ============================================================
# 7. NumPy Academic Demonstrations
# ============================================================

def compute_numpy_stats(series: pd.Series) -> dict:
    """
    Calculate rigorous descriptive statistics using NumPy explicitly.
    Demonstrates NumPy array operations for the academic project.
    """
    clean_series = pd.to_numeric(series.dropna(), errors="coerce").dropna()
    arr = np.array(clean_series, dtype=float)
    if len(arr) == 0:
        return {
            "count": 0, "mean": 0.0, "median": 0.0, "std": 0.0,
            "min": 0.0, "max": 0.0, "q25": 0.0, "q75": 0.0, "iqr": 0.0
        }

    q25, q75 = np.percentile(arr, [25, 75])
    return {
        "count":  int(len(arr)),
        "mean":   float(np.mean(arr)),
        "median": float(np.median(arr)),
        "std":    float(np.std(arr)),
        "min":    float(np.min(arr)),
        "max":    float(np.max(arr)),
        "q25":    float(q25),
        "q75":    float(q75),
        "iqr":    float(q75 - q25),
    }


def normalise_series(series: pd.Series) -> np.ndarray:
    """Min-max normalize a series using NumPy."""
    arr = np.array(pd.to_numeric(series, errors="coerce").fillna(0.0), dtype=float)
    mn, mx = np.min(arr), np.max(arr)
    if mx == mn:
        return np.zeros_like(arr)
    return (arr - mn) / (mx - mn)
