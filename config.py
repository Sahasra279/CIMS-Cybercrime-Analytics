# ============================================================
# config.py — Centralised application configuration
# Cybercrime Incident Management System (CIMS)
# Cybercrime Analytics & Visualization System
# ============================================================

import os

# ── Application metadata ─────────────────────────────────────
APP_TITLE       = "Cybercrime Analytics & Visualization System"
APP_SHORT_TITLE = "CIMS Analytics"
APP_VERSION     = "2.0.0 (CSV Edition)"
APP_ICON        = "🔐"

# ── Page layout ──────────────────────────────────────────────
PAGE_LAYOUT      = "wide"
SIDEBAR_STATE    = "expanded"

# ── Data source paths (CSV files) ─────────────────────────────
BASE_DIR         = os.path.dirname(os.path.abspath(__file__))
DATA_DIR         = os.path.join(BASE_DIR, "data")

INCIDENTS_CSV    = os.path.join(DATA_DIR, "incidents.csv")
CASES_CSV        = os.path.join(DATA_DIR, "cases.csv")
EVIDENCE_CSV     = os.path.join(DATA_DIR, "evidence.csv")
USERS_CSV        = os.path.join(DATA_DIR, "users.csv")
AUDIT_LOGS_CSV   = os.path.join(DATA_DIR, "audit_logs.csv")

# ── Colour palette (matches assets/styles.css) ───────────────
COLORS = {
    "bg_primary":    "#0a0e1a",
    "bg_secondary":  "#111827",
    "bg_card":       "#1a2235",
    "accent_cyan":   "#00d4ff",
    "accent_blue":   "#3b82f6",
    "accent_purple": "#8b5cf6",
    "accent_green":  "#10b981",
    "accent_red":    "#ef4444",
    "accent_yellow": "#f59e0b",
    "text_primary":  "#e2e8f0",
    "text_secondary":"#94a3b8",
}

# Plotly-compatible colour sequences for multi-series charts
PLOTLY_COLOR_SEQUENCE = [
    "#00d4ff", "#3b82f6", "#8b5cf6",
    "#10b981", "#f59e0b", "#ef4444",
    "#ec4899", "#14b8a6",
]

# Matplotlib/Seaborn compatible colour palette
MPL_PALETTE = [
    "#00d4ff", "#3b82f6", "#8b5cf6",
    "#10b981", "#f59e0b", "#ef4444",
]

# ── Chart defaults ────────────────────────────────────────────
CHART_BG_COLOR   = "#111827"
CHART_PAPER_BG   = "#0a0e1a"
CHART_FONT_COLOR = "#e2e8f0"
CHART_GRID_COLOR = "#1e3a5f"

# ── Sidebar navigation entries ────────────────────────────────
NAV_PAGES = [
    {"icon": "🏠", "label": "CIMS Dashboard",          "file": "app.py"},
    {"icon": "🔍", "label": "Crime Analysis",          "file": "pages/1_Crime_Analysis.py"},
    {"icon": "📈", "label": "Trend Analysis",          "file": "pages/2_Trend_Analysis.py"},
    {"icon": "💰", "label": "Financial Analysis",      "file": "pages/3_Financial_Analysis.py"},
    {"icon": "📊", "label": "Statistical Analysis",    "file": "pages/4_Statistical_Analysis.py"},
    {"icon": "🗂️",  "label": "Dataset & Case Explorer", "file": "pages/5_Dataset_Explorer.py"},
]

# ── Crime types & metadata ────────────────────────────────────
CRIME_TYPES = [
    "Phishing",
    "Ransomware",
    "Identity Theft",
    "Online Fraud",
    "Data Breach",
    "Cyberstalking",
    "Hacking",
    "Social Engineering",
    "DDoS Attack",
    "Financial Fraud",
]

INCIDENT_STATUSES = ["Reported", "Under Investigation", "Resolved", "Pending"]
CASE_STATUSES     = ["Open", "Under Investigation", "Closed"]
PRIORITY_LEVELS   = ["Low", "Medium", "High", "Critical"]
