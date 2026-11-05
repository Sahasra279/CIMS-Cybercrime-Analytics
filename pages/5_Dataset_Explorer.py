# ============================================================
# pages/5_Dataset_Explorer.py
# Cybercrime Incident Management System (CIMS)
# Cybercrime Analytics & Visualization System
# ============================================================

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
import pandas as pd
from datetime import datetime, date

from config import APP_ICON, APP_SHORT_TITLE, CRIME_TYPES, PRIORITY_LEVELS, INCIDENT_STATUSES, CASE_STATUSES
from utils.data_processing import (
    load_all_datasets,
    save_dataset,
    update_record,
    delete_record,
    log_audit_action,
    render_global_sidebar_filters,
    render_filter_summary_badge,
    search_dataframe,
)

st.set_page_config(page_title=f"{APP_SHORT_TITLE} | Dataset Explorer", page_icon="🗂️", layout="wide")

css_path = os.path.join(os.path.dirname(__file__), "..", "assets", "styles.css")
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ── Load Datasets & Global Sidebar Filters ─────────────────────
datasets = load_all_datasets()
incidents_raw = datasets["incidents"]
cases = datasets["cases"]
evidence = datasets["evidence"]
users = datasets["users"]
audit_logs = datasets["audit_logs"]

with st.sidebar:
    st.markdown(f"## {APP_ICON} {APP_SHORT_TITLE}")
    st.caption("CIMS Management & Explorer")
    st.markdown("---")

filtered_incidents, active_filters = render_global_sidebar_filters(incidents_raw, cases)


# ── Page Header ───────────────────────────────────────────────
st.markdown(
    """
    <div class="page-header">
        <h1>🗂️ CIMS Dataset Explorer & CRUD Management</h1>
        <p>Interactive search, dynamic column selection, complete record lifecycle management (Create, Read, Update, Delete), and CSV export.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

render_filter_summary_badge(filtered_incidents, len(incidents_raw), active_filters)

# ── Management Tabs ───────────────────────────────────────────
tab_incidents, tab_cases, tab_evidence, tab_users, tab_audit = st.tabs([
    "🗂️ Incident Management",
    "💼 Case Management",
    "🔬 Evidence Management",
    "👥 User Management",
    "📜 Audit Logs",
])


# ============================================================
# TAB 1: INCIDENT MANAGEMENT (CRUD)
# ============================================================
with tab_incidents:
    st.markdown("### 🗂️ Incident Records & Search")

    # Search & Column Selection Toolbar
    search_col1, search_col2 = st.columns([1.6, 1])
    with search_col1:
        query_inc = st.text_input(
            "🔍 Search Incidents",
            placeholder="Search by Incident ID, Case ID, Crime Type, Status, City, State, Channel...",
            key="search_incidents_input",
            help="Instant search across all text attributes",
        )
    with search_col2:
        all_inc_cols = [
            "incident_id", "case_id", "reported_date", "incident_type",
            "channel", "city", "state", "financial_loss_inr", "priority", "status", "assigned_user_id"
        ]
        selected_cols = st.multiselect(
            "📋 Columns to Display",
            options=all_inc_cols,
            default=all_inc_cols,
            key="inc_col_select",
        )

    searchable_cols = ["incident_id", "case_id", "incident_type", "channel", "city", "state", "priority", "status", "assigned_user_id"]
    display_incidents = search_dataframe(filtered_incidents, query_inc, searchable_cols)

    if not selected_cols:
        selected_cols = all_inc_cols

    cols_to_show = [c for c in selected_cols if c in display_incidents.columns]
    st.caption(f"Displaying **{len(display_incidents)}** matching records (from {len(filtered_incidents)} filtered, {len(incidents_raw)} total in CSV).")
    st.dataframe(display_incidents[cols_to_show], use_container_width=True)

    # Download CSV button
    csv_data = display_incidents[cols_to_show].to_csv(index=False).encode("utf-8")
    st.download_button(
        "💾 Download Matching Incidents (CSV)",
        data=csv_data,
        file_name="cims_filtered_incidents.csv",
        mime="text/csv",
    )

    st.markdown("---")

    # CRUD Operations Accordion
    c_add, c_edit, c_del = st.columns(3)

    # 1. Add Incident
    with c_add:
        with st.expander("➕ Log New Incident", expanded=False):
            with st.form("add_incident_form", clear_on_submit=True):
                next_inc_id = f"INC-2024-{len(incidents_raw) + 1:03d}"
                next_case_id = f"CAS-2024-{len(cases) + 1:03d}"
                
                f_id = st.text_input("Incident ID", value=next_inc_id)
                f_date = st.date_input("Reported Date", value=date.today())
                f_type = st.selectbox("Crime Type", options=CRIME_TYPES)
                f_chan = st.selectbox("Channel", options=["Email", "Web Portal", "Mobile App", "Phone/VoIP", "Cloud Storage", "Network Intrusions", "VPN Gateway", "Social Media"])
                f_loss = st.number_input("Loss (INR)", min_value=0.0, step=10000.0, value=50000.0)
                f_city = st.text_input("City", value="Mumbai")
                f_state = st.text_input("State", value="Maharashtra")
                f_prio = st.selectbox("Priority", options=PRIORITY_LEVELS)
                f_stat = st.selectbox("Status", options=INCIDENT_STATUSES)
                f_user = st.selectbox("Investigator", options=users["user_id"].tolist() if not users.empty else ["USR-101"])
                f_case = st.text_input("Case ID", value=next_case_id)

                submit_inc = st.form_submit_button("Record Incident")
                if submit_inc:
                    new_row = pd.DataFrame([{
                        "incident_id": f_id,
                        "reported_date": f_date.strftime("%Y-%m-%d"),
                        "incident_type": f_type,
                        "channel": f_chan,
                        "city": f_city,
                        "state": f_state,
                        "financial_loss_inr": f_loss,
                        "priority": f_prio,
                        "status": f_stat,
                        "assigned_user_id": f_user,
                        "case_id": f_case,
                    }])
                    updated_inc = pd.concat([incidents_raw, new_row], ignore_index=True)
                    if save_dataset("incidents", updated_inc):
                        log_audit_action(f_user, f_id, f"Logged incident {f_id} ({f_type})")
                        st.success(f"Incident {f_id} created and persisted to CSV!")
                        st.rerun()

    # 2. Edit Incident
    with c_edit:
        with st.expander("✏️ Update Incident Record", expanded=False):
            if not incidents_raw.empty:
                inc_list = incidents_raw["incident_id"].tolist()
                selected_edit_inc = st.selectbox("Select Incident to Edit", options=inc_list, key="edit_inc_selector")
                
                # Fetch current record values
                curr_row = incidents_raw[incidents_raw["incident_id"] == selected_edit_inc].iloc[0]
                
                with st.form("edit_incident_form"):
                    e_stat_idx = INCIDENT_STATUSES.index(curr_row["status"]) if curr_row["status"] in INCIDENT_STATUSES else 0
                    e_status = st.selectbox("Updated Status", options=INCIDENT_STATUSES, index=e_stat_idx)
                    
                    e_prio_idx = PRIORITY_LEVELS.index(curr_row["priority"]) if curr_row["priority"] in PRIORITY_LEVELS else 0
                    e_priority = st.selectbox("Updated Priority", options=PRIORITY_LEVELS, index=e_prio_idx)
                    
                    e_loss = st.number_input("Updated Loss (INR)", min_value=0.0, step=10000.0, value=float(curr_row["financial_loss_inr"]))
                    
                    user_list = users["user_id"].tolist() if not users.empty else ["USR-101"]
                    e_u_idx = user_list.index(curr_row["assigned_user_id"]) if curr_row["assigned_user_id"] in user_list else 0
                    e_user = st.selectbox("Reassign Investigator", options=user_list, index=e_u_idx)

                    submit_edit = st.form_submit_button("Save Changes to CSV")
                    if submit_edit:
                        updated_fields = {
                            "status": e_status,
                            "priority": e_priority,
                            "financial_loss_inr": e_loss,
                            "assigned_user_id": e_user,
                        }
                        if update_record("incidents", "incident_id", selected_edit_inc, updated_fields):
                            log_audit_action(e_user, selected_edit_inc, f"Updated incident {selected_edit_inc} (Status: {e_status}, Prio: {e_priority})")
                            st.success(f"Incident {selected_edit_inc} updated successfully!")
                            st.rerun()
            else:
                st.info("No incident records available to edit.")

    # 3. Delete Incident
    with c_del:
        with st.expander("🗑️ Delete Incident Record", expanded=False):
            if not incidents_raw.empty:
                del_inc_id = st.selectbox("Select Incident to Delete", options=incidents_raw["incident_id"].tolist(), key="del_inc_selector")
                confirm_del = st.checkbox(f"Confirm deletion of {del_inc_id}", key="confirm_del_inc")
                if st.button("Delete Incident Permanently", type="secondary"):
                    if confirm_del:
                        if delete_record("incidents", "incident_id", del_inc_id):
                            log_audit_action("SYSTEM", del_inc_id, f"Deleted incident {del_inc_id}")
                            st.success(f"Incident {del_inc_id} removed from incidents.csv!")
                            st.rerun()
                    else:
                        st.error("Please check the confirmation box before deleting.")
            else:
                st.info("No records to delete.")


# ============================================================
# TAB 2: CASE MANAGEMENT (CRUD)
# ============================================================
with tab_cases:
    st.markdown("### 💼 Investigation Cases & Dossiers")

    col_case_s1, col_case_s2 = st.columns([1.6, 1])
    with col_case_s1:
        query_cases = st.text_input("🔍 Search Cases", placeholder="Search by Case ID, Incident ID, Title, Status...", key="search_cases_input")
    with col_case_s2:
        all_case_cols = cases.columns.tolist()
        sel_case_cols = st.multiselect("Columns to Display", options=all_case_cols, default=all_case_cols, key="case_col_select")

    display_cases = search_dataframe(cases, query_cases)
    show_case_cols = [c for c in sel_case_cols if c in display_cases.columns] if sel_case_cols else all_case_cols

    st.caption(f"Displaying **{len(display_cases)}** of {len(cases)} cases.")
    st.dataframe(display_cases[show_case_cols], use_container_width=True)

    csv_cases = display_cases[show_case_cols].to_csv(index=False).encode("utf-8")
    st.download_button(
        "💾 Download Cases (CSV)",
        data=csv_cases,
        file_name="cims_cases.csv",
        mime="text/csv",
    )

    st.markdown("---")

    case_add, case_edit, case_del = st.columns(3)

    # 1. Add Case
    with case_add:
        with st.expander("➕ Open New Case File", expanded=False):
            with st.form("add_case_form", clear_on_submit=True):
                next_case_num = f"CAS-2024-{len(cases) + 1:03d}"
                c_id = st.text_input("Case ID", value=next_case_num)
                c_inc = st.selectbox("Linked Incident ID", options=incidents_raw["incident_id"].tolist() if not incidents_raw.empty else [])
                c_title = st.text_input("Case Title / Dossier Name", value="Investigation of Threat Vector")
                c_status = st.selectbox("Case Status", options=CASE_STATUSES)
                c_assigned = st.selectbox("Lead Investigator", options=users["user_id"].tolist() if not users.empty else ["USR-101"])
                c_created = st.date_input("Creation Date", value=date.today())

                submit_case = st.form_submit_button("Create Case Dossier")
                if submit_case:
                    new_case = pd.DataFrame([{
                        "case_id": c_id,
                        "incident_id": c_inc,
                        "case_title": c_title,
                        "case_status": c_status,
                        "assigned_user_id": c_assigned,
                        "created_date": c_created.strftime("%Y-%m-%d"),
                        "closed_date": "",
                    }])
                    updated_cases = pd.concat([cases, new_case], ignore_index=True)
                    if save_dataset("cases", updated_cases):
                        log_audit_action(c_assigned, c_id, f"Created new case dossier {c_id}")
                        st.success(f"Case {c_id} created and persisted to CSV!")
                        st.rerun()

    # 2. Edit Case Status
    with case_edit:
        with st.expander("✏️ Update Case Dossier", expanded=False):
            if not cases.empty:
                sel_edit_case = st.selectbox("Select Case to Update", options=cases["case_id"].tolist(), key="edit_case_sel")
                curr_case_row = cases[cases["case_id"] == sel_edit_case].iloc[0]
                
                with st.form("edit_case_form"):
                    stat_idx = CASE_STATUSES.index(curr_case_row["case_status"]) if curr_case_row["case_status"] in CASE_STATUSES else 0
                    new_case_stat = st.selectbox("Update Case Status", options=CASE_STATUSES, index=stat_idx)
                    new_case_title = st.text_input("Case Title", value=str(curr_case_row["case_title"]))
                    is_closed = (new_case_stat in ["Closed", "Resolved"])
                    close_date = date.today().strftime("%Y-%m-%d") if is_closed else ""

                    submit_case_edit = st.form_submit_button("Update Case Record")
                    if submit_case_edit:
                        updated_case_fields = {
                            "case_status": new_case_stat,
                            "case_title": new_case_title,
                            "closed_date": close_date,
                        }
                        if update_record("cases", "case_id", sel_edit_case, updated_case_fields):
                            log_audit_action(curr_case_row["assigned_user_id"], sel_edit_case, f"Updated case status to {new_case_stat}")
                            st.success(f"Case {sel_edit_case} updated to {new_case_stat}!")
                            st.rerun()
            else:
                st.info("No cases available to edit.")

    # 3. Delete Case
    with case_del:
        with st.expander("🗑️ Delete Case File", expanded=False):
            if not cases.empty:
                del_case_id = st.selectbox("Select Case to Delete", options=cases["case_id"].tolist(), key="del_case_sel")
                confirm_del_c = st.checkbox(f"Confirm deletion of {del_case_id}", key="confirm_del_case")
                if st.button("Delete Case File", key="btn_del_case"):
                    if confirm_del_c:
                        if delete_record("cases", "case_id", del_case_id):
                            log_audit_action("SYSTEM", del_case_id, f"Deleted case {del_case_id}")
                            st.success(f"Case {del_case_id} removed from cases.csv!")
                            st.rerun()
                    else:
                        st.error("Please confirm before deleting.")
            else:
                st.info("No cases to delete.")


# ============================================================
# TAB 3: EVIDENCE MANAGEMENT (CRUD)
# ============================================================
with tab_evidence:
    st.markdown("### 🔬 Forensic Evidence Repository")

    col_ev_s1, col_ev_s2 = st.columns([1.6, 1])
    with col_ev_s1:
        query_ev = st.text_input("🔍 Search Evidence", placeholder="Search by Evidence ID, Case ID, Description, Category, Verification Status...", key="search_ev_input")
    with col_ev_s2:
        all_ev_cols = evidence.columns.tolist()
        sel_ev_cols = st.multiselect("Columns to Display", options=all_ev_cols, default=all_ev_cols, key="ev_col_select")

    display_ev = search_dataframe(evidence, query_ev)
    show_ev_cols = [c for c in sel_ev_cols if c in display_ev.columns] if sel_ev_cols else all_ev_cols

    st.caption(f"Displaying **{len(display_ev)}** of {len(evidence)} evidence records.")
    st.dataframe(display_ev[show_ev_cols], use_container_width=True)

    csv_evid = display_ev[show_ev_cols].to_csv(index=False).encode("utf-8")
    st.download_button(
        "💾 Download Evidence (CSV)",
        data=csv_evid,
        file_name="cims_evidence.csv",
        mime="text/csv",
    )

    st.markdown("---")

    ev_add, ev_edit, ev_del = st.columns(3)

    # 1. Add Evidence
    with ev_add:
        with st.expander("➕ Log Evidence Item", expanded=False):
            with st.form("add_evidence_form", clear_on_submit=True):
                next_evd_id = f"EVD-{len(evidence) + 301}"
                e_id = st.text_input("Evidence ID", value=next_evd_id)
                e_case = st.selectbox("Associated Case ID", options=cases["case_id"].tolist() if not cases.empty else ["CAS-2024-001"])
                e_desc = st.text_area("Evidence Description", placeholder="e.g. Memory dump, PCAP capture, header trace")
                e_type = st.selectbox("Evidence Category", options=["Digital Log", "Malware Binary", "PCAP File", "Digital Document", "Script Code", "Transaction Record", "Audit Log", "System Log", "Financial Record", "Email Record"])
                e_date = st.date_input("Collection Date", value=date.today())
                e_collector = st.selectbox("Collected By User", options=users["user_id"].tolist() if not users.empty else ["USR-101"])
                e_ver = st.selectbox("Verification Status", options=["Pending Review", "Verified", "Rejected"])

                submit_evd = st.form_submit_button("Submit Evidence Record")
                if submit_evd:
                    new_evd = pd.DataFrame([{
                        "evidence_id": e_id,
                        "case_id": e_case,
                        "evidence_description": e_desc,
                        "evidence_type": e_type,
                        "collected_date": e_date.strftime("%Y-%m-%d"),
                        "collected_by_user_id": e_collector,
                        "verification_status": e_ver,
                    }])
                    updated_evd = pd.concat([evidence, new_evd], ignore_index=True)
                    if save_dataset("evidence", updated_evd):
                        log_audit_action(e_collector, e_id, f"Registered evidence {e_id} for {e_case}")
                        st.success(f"Evidence {e_id} successfully recorded!")
                        st.rerun()

    # 2. Update Evidence Status
    with ev_edit:
        with st.expander("✏️ Update Evidence Verification", expanded=False):
            if not evidence.empty:
                sel_edit_ev = st.selectbox("Select Evidence to Update", options=evidence["evidence_id"].tolist(), key="edit_ev_sel")
                curr_ev_row = evidence[evidence["evidence_id"] == sel_edit_ev].iloc[0]
                
                with st.form("edit_ev_form"):
                    ev_stat_opts = ["Pending Review", "Verified", "Rejected"]
                    v_idx = ev_stat_opts.index(curr_ev_row["verification_status"]) if curr_ev_row["verification_status"] in ev_stat_opts else 0
                    new_ver_status = st.selectbox("Verification Status", options=ev_stat_opts, index=v_idx)
                    new_ev_desc = st.text_area("Description / Notes", value=str(curr_ev_row["evidence_description"]))

                    submit_ev_edit = st.form_submit_button("Update Evidence Status")
                    if submit_ev_edit:
                        updated_ev_fields = {
                            "verification_status": new_ver_status,
                            "evidence_description": new_ev_desc,
                        }
                        if update_record("evidence", "evidence_id", sel_edit_ev, updated_ev_fields):
                            log_audit_action(curr_ev_row["collected_by_user_id"], sel_edit_ev, f"Updated evidence {sel_edit_ev} to {new_ver_status}")
                            st.success(f"Evidence {sel_edit_ev} updated to {new_ver_status}!")
                            st.rerun()
            else:
                st.info("No evidence records available to edit.")

    # 3. Delete Evidence
    with ev_del:
        with st.expander("🗑️ Delete Evidence Item", expanded=False):
            if not evidence.empty:
                del_ev_id = st.selectbox("Select Evidence to Delete", options=evidence["evidence_id"].tolist(), key="del_ev_sel")
                confirm_del_e = st.checkbox(f"Confirm deletion of {del_ev_id}", key="confirm_del_ev")
                if st.button("Delete Evidence Record", key="btn_del_ev"):
                    if confirm_del_e:
                        if delete_record("evidence", "evidence_id", del_ev_id):
                            log_audit_action("SYSTEM", del_ev_id, f"Deleted evidence {del_ev_id}")
                            st.success(f"Evidence {del_ev_id} removed from evidence.csv!")
                            st.rerun()
                    else:
                        st.error("Please confirm before deleting.")
            else:
                st.info("No evidence records to delete.")


# ============================================================
# TAB 4: USER MANAGEMENT (CRUD)
# ============================================================
with tab_users:
    st.markdown("### 👥 System Users & Investigators")

    query_user = st.text_input("🔍 Search Users", placeholder="Search by User ID, Name, Role, Email, Status...", key="search_user_input")
    display_users = search_dataframe(users, query_user)
    st.caption(f"Displaying **{len(display_users)}** of {len(users)} users.")
    st.dataframe(display_users, use_container_width=True)

    csv_users = display_users.to_csv(index=False).encode("utf-8")
    st.download_button(
        "💾 Download Users (CSV)",
        data=csv_users,
        file_name="cims_users.csv",
        mime="text/csv",
    )

    st.markdown("---")

    usr_add, usr_edit, usr_del = st.columns(3)

    # 1. Add User
    with usr_add:
        with st.expander("➕ Register New User Profile", expanded=False):
            with st.form("add_user_form", clear_on_submit=True):
                next_usr_id = f"USR-{len(users) + 101}"
                u_id = st.text_input("User ID", value=next_usr_id)
                u_name = st.text_input("Full Name", placeholder="e.g. Inspector Neha Deshmukh")
                u_role = st.selectbox("Role", options=["Lead Cyber Investigator", "Senior Forensic Analyst", "Cyber Threat Analyst", "Junior Security Analyst", "Investigative Auditor"])
                u_email = st.text_input("Official Email", placeholder="user@cims-agency.gov.in")
                u_status = st.selectbox("Account Status", options=["Active", "On Leave", "Suspended"])

                submit_user = st.form_submit_button("Save User Profile")
                if submit_user:
                    new_usr = pd.DataFrame([{
                        "user_id": u_id,
                        "full_name": u_name,
                        "role": u_role,
                        "email": u_email,
                        "account_status": u_status,
                    }])
                    updated_users = pd.concat([users, new_usr], ignore_index=True)
                    if save_dataset("users", updated_users):
                        log_audit_action("SYSTEM", u_id, f"Registered new user {u_name} ({u_id})")
                        st.success(f"User {u_name} ({u_id}) registered successfully!")
                        st.rerun()

    # 2. Update User
    with usr_edit:
        with st.expander("✏️ Update User Account", expanded=False):
            if not users.empty:
                sel_edit_usr = st.selectbox("Select User to Update", options=users["user_id"].tolist(), key="edit_usr_sel")
                curr_usr_row = users[users["user_id"] == sel_edit_usr].iloc[0]
                
                with st.form("edit_usr_form"):
                    u_roles = ["Lead Cyber Investigator", "Senior Forensic Analyst", "Cyber Threat Analyst", "Junior Security Analyst", "Investigative Auditor"]
                    r_idx = u_roles.index(curr_usr_row["role"]) if curr_usr_row["role"] in u_roles else 0
                    new_role = st.selectbox("Role", options=u_roles, index=r_idx)
                    
                    u_stats = ["Active", "On Leave", "Suspended"]
                    s_idx = u_stats.index(curr_usr_row["account_status"]) if curr_usr_row["account_status"] in u_stats else 0
                    new_acc_stat = st.selectbox("Account Status", options=u_stats, index=s_idx)

                    submit_usr_edit = st.form_submit_button("Update User Profile")
                    if submit_usr_edit:
                        updated_usr_fields = {
                            "role": new_role,
                            "account_status": new_acc_stat,
                        }
                        if update_record("users", "user_id", sel_edit_usr, updated_usr_fields):
                            log_audit_action("ADMIN", sel_edit_usr, f"Updated user {sel_edit_usr} (Role: {new_role}, Status: {new_acc_stat})")
                            st.success(f"User {sel_edit_usr} updated successfully!")
                            st.rerun()
            else:
                st.info("No users available to edit.")

    # 3. Deactivate User
    with usr_del:
        with st.expander("🗑️ Deactivate User", expanded=False):
            if not users.empty:
                del_usr_id = st.selectbox("Select User to Deactivate", options=users["user_id"].tolist(), key="del_usr_sel")
                confirm_del_u = st.checkbox(f"Confirm deactivation of {del_usr_id}", key="confirm_del_usr")
                if st.button("Deactivate Account", key="btn_del_usr"):
                    if confirm_del_u:
                        if update_record("users", "user_id", del_usr_id, {"account_status": "Suspended"}):
                            log_audit_action("ADMIN", del_usr_id, f"Suspended account for user {del_usr_id}")
                            st.success(f"User {del_usr_id} marked as Suspended in users.csv!")
                            st.rerun()
                    else:
                        st.error("Please confirm before deactivating.")
            else:
                st.info("No users to deactivate.")


# ============================================================
# TAB 5: AUDIT LOGS
# ============================================================
with tab_audit:
    st.markdown("### 📜 System Audit Trail")
    st.caption("Immutable chronological record of all administrative, case update, evidence logging, and CRUD events.")

    query_audit = st.text_input("🔍 Search Audit Trail", placeholder="Search by Action, Reference ID, User ID...", key="search_audit_input")
    display_audit = search_dataframe(audit_logs, query_audit).sort_values("timestamp", ascending=False)
    st.caption(f"Displaying **{len(display_audit)}** of {len(audit_logs)} audit records.")
    st.dataframe(display_audit, use_container_width=True)

    csv_audit = display_audit.to_csv(index=False).encode("utf-8")
    st.download_button(
        "💾 Download Audit Logs (CSV)",
        data=csv_audit,
        file_name="cims_audit_logs.csv",
        mime="text/csv",
    )
