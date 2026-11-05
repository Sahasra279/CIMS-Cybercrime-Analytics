# 🔐 Cybercrime Analytics & Visualization System (CAVS)
### Cybercrime Incident Management System (CIMS)

> **Academic Project** — Data Visualization Subject · B.Tech · 2026  
> A complete, responsive Python + Streamlit cybercrime analytics platform powered exclusively by local, interconnected CSV data stores.

---

## 📋 Project Overview

The **Cybercrime Analytics & Visualization System (CAVS)** is an executive intelligence and incident management dashboard designed to assist cybercrime cells, investigators, and decision-makers. It unifies incident tracking, investigative case files, forensic evidence custody, and quantitative financial loss evaluation into an intuitive, responsive dark-themed web application.

The application operates in **100% pure local CSV mode** without requiring any external database engines (such as MySQL, PostgreSQL, or cloud services like Aiven). All CRUD operations persist directly to structured CSV files with an immutable chronological audit trail.

---

## ✨ Main Features

- 🏠 **Executive CIMS Dashboard:**
  - Real-time KPI indicator cards (Total Incidents, Total Cases, Active Cases, Resolved Cases, Cumulative Financial Loss).
  - Responsive 2-column layout preventing horizontal clipping or overflow across desktop viewports.
  - Interactive Plotly figures: Crime Classification Bar Chart, Incident Status Donut, Priority Severity Spread, Monthly Inflow Trajectory, Categorical Loss Breakdown, and Active Case Pipeline.
- 🎛️ **Unified Global Sidebar Filters:**
  - Calendar Date Range Filter bounded by actual incident dates.
  - Crime / Incident Type Dropdown (`All` + dynamic category selection).
  - Incident Status Dropdown (`All`, `Reported`, `Under Investigation`, `Resolved`, `Pending`).
  - Priority Severity Dropdown (`All`, `Critical`, `High`, `Medium`, `Low`).
  - State / Location Dropdown (`All` + metropolitan states/cities).
  - One-click `🔄 Clear All Filters` reset button.
  - Persistent state synchronization across all application pages via `st.session_state`.
- 🔍 **Incident Crime Analysis (`pages/1_Crime_Analysis.py`):**
  - Attack delivery vector distribution (Email, Web, Mobile App, VoIP, Cloud, Network).
  - Geographic state and city crime volume visualization.
  - Cross-tabulated Priority vs. Resolution Status matrix heatmap (Seaborn) and Matplotlib static plots.
- 📈 **Temporal Trend Analysis (`pages/2_Trend_Analysis.py`):**
  - Month-over-month incident volume progression.
  - Monthly financial exposure trajectory.
  - Pandas dynamic pivot tables for attack vectors over time.
  - Mathematical moving average smoothing powered by **NumPy** arrays and Matplotlib.
- 💰 **Financial Impact Analysis (`pages/3_Financial_Analysis.py`):**
  - Total and average financial loss quantification.
  - Proportional hierarchical Treemap (`State → Attack Vector`).
  - Top 8 high-impact cybercrime case ranking.
  - Loss dispersion and outlier detection using Seaborn boxplots.
  - Rigorous **NumPy** statistical summary (Mean, Median, Std Dev, Q1, Q3, IQR, Maximum).
- 📊 **Statistical Analysis & Data Science (`pages/4_Statistical_Analysis.py`):**
  - Feature engineering and Pearson correlation coefficient matrix (Seaborn heatmap).
  - Kernel Density Estimation (KDE) and probability density curve (Seaborn histogram).
  - Explicit NumPy matrix operations, standard deviations, and Min-Max feature normalization.
  - Multi-dimensional Plotly scatter analysis.
- 🗂️ **Dataset Explorer & Full CRUD Management (`pages/5_Dataset_Explorer.py`):**
  - **Instant Multi-Column Search:** Live keyword matching across Incident ID, Case ID, Crime Type, Status, City, State, Channel, Priority, and Assigned Investigator.
  - **Custom Column Selection:** Interactive multiselect to display and export only desired fields.
  - **Full Lifecycle CRUD Forms:**
    - ➕ **Create:** Forms to record new incidents, open case files, register evidence, and add users.
    - 📖 **Read:** Instant tabular views with matching record counters.
    - ✏️ **Update:** Select any existing record to modify statuses, reassign investigators, or update financial losses.
    - 🗑️ **Delete:** Safe record deletion with explicit confirmation checkboxes.
  - **Persistent CSV Export:** One-click download button for filtered and searched subsets.
  - **Audit Trail Monitoring:** Chronological activity logging of all administrative and CRUD actions.

---

## 🛠️ Technology Stack

| Layer | Technologies |
|-------|--------------|
| **Core Framework** | Python 3.11+ · Streamlit (v1.38+) |
| **Data Engine** | Pandas (CSV ingestion, filtering, pivot tables, cross-tabulation) |
| **Numerical Computations** | NumPy (Array vectorization, moving averages, percentiles, normalization) |
| **Interactive Visualizations** | Plotly Express & Plotly Graph Objects (Responsive dark theme) |
| **Academic Statistical Plots** | Matplotlib & Seaborn (Heatmaps, Boxplots, KDE histograms, Static bars) |
| **Styling & Design** | Custom CSS (`assets/styles.css`) — Navy/Black dark mode with Cyan, Blue, and Purple accents |

---

## 📁 Project Folder Structure

```
Cybercrime-Analytics/
├── app.py                      # Executive Dashboard & Global Filter System
├── config.py                   # Central constants, color schemes & data paths
├── requirements.txt            # Python package dependencies
├── README.md                   # Project documentation & setup manual
├── DEMO_GUIDE.md               # Step-by-step presentation & evaluation script
│
├── assets/
│   └── styles.css              # Dark theme CSS stylesheet (responsive & fitted)
│
├── data/                       # Local CSV Data Store
│   ├── incidents.csv           # Cybercrime incident reports
│   ├── cases.csv               # Formal investigative case dossiers
│   ├── evidence.csv            # Forensic digital & physical evidence custody
│   ├── users.csv               # Department investigators and analysts
│   ├── audit_logs.csv          # Immutable system activity trail
│   └── backup/                 # Pristine copy of sample demonstration datasets
│
├── pages/                      # Streamlit Multi-Page Routes
│   ├── 1_Crime_Analysis.py     # Attack vectors, channels, state/city breakdowns
│   ├── 2_Trend_Analysis.py     # Monthly progressions & NumPy moving averages
│   ├── 3_Financial_Analysis.py # Loss Treemap, ranking & NumPy dispersion
│   ├── 4_Statistical_Analysis.py # Correlation matrix, KDE & Min-Max scaling
│   └── 5_Dataset_Explorer.py   # Multi-tab CRUD suite with instant search & export
│
└── utils/
    ├── data_processing.py      # CSV loaders, shared filters, search, CRUD & KPIs
    └── visualizations.py       # Plotly, Seaborn, and Matplotlib chart generators
```

---

## 💾 Explanation of CSV Data Files

The system uses 5 relational CSV files in [`data/`](file:///c:/Users/sahas/OneDrive/Desktop/cybercrime/Cybercrime-Analytics/data):

| File | Primary Key | Foreign Keys | Key Attributes & Description |
|------|-------------|--------------|------------------------------|
| **`incidents.csv`** | `incident_id` | `case_id`, `assigned_user_id` | Incident report details: `reported_date`, `incident_type`, `channel`, `city`, `state`, `financial_loss_inr`, `priority`, `status`. |
| **`cases.csv`** | `case_id` | `incident_id`, `assigned_user_id` | Formal investigation files: `case_title`, `case_status` (`Open`, `Under Investigation`, `Closed`), `created_date`, `closed_date`. |
| **`evidence.csv`** | `evidence_id` | `case_id`, `collected_by_user_id` | Chain of custody records: `evidence_description`, `evidence_type` (PCAP, Malware Binary, Digital Log, etc.), `collected_date`, `verification_status` (`Pending Review`, `Verified`, `Rejected`). |
| **`users.csv`** | `user_id` | — | Personnel profiles: `full_name`, `role` (Lead Investigator, Forensic Analyst, etc.), `email`, `account_status` (`Active`, `On Leave`, `Suspended`). |
| **`audit_logs.csv`** | `log_id` | `user_id`, `record_reference` | Chronological audit trail: `action`, `timestamp`. Records every creation, update, and deletion event. |

---

## 🚀 Setup & Execution Instructions

### Prerequisites
- Python 3.11 or newer installed on your system.
- `pip` package manager available on your command line.

### Step 1: Open Terminal / PowerShell
Navigate into the project directory:
```powershell
cd "c:\Users\sahas\OneDrive\Desktop\cybercrime\Cybercrime-Analytics"
```

### Step 2: Activate the Virtual Environment
**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```
*(If script execution is restricted, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` or directly invoke `.\venv\Scripts\streamlit.exe`)*

**macOS / Linux:**
```bash
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the Application
```powershell
streamlit run app.py
```
The application will launch automatically in your web browser at:
👉 **`http://localhost:8501`**

Press `Ctrl + C` in your terminal to stop the application server.

---

## 🔑 Authentication & Login Notice

> **Access Mode:** This academic demonstration project operates in **Open Demonstration Mode**.  
> User authentication (passwords / tokens) is intentionally bypassed so evaluators and students can inspect all modules freely without credential friction.
>
> Sample user profiles available for assigning cases and evidence:
> - `USR-101` — **Rajesh Kumar** (Lead Cyber Investigator)
> - `USR-102` — **Priya Sharma** (Senior Forensic Analyst)
> - `USR-103` — **Amit Verma** (Cyber Threat Analyst)
> - `USR-104` — **Sneha Patel** (Junior Security Analyst)

---

## ⚠️ Important Limitations & Synthetic Data Disclaimer

1. **Synthetic Data Disclaimer:** All incidents, cases, financial amounts, IP logs, names, and contact emails contained in the `data/` directory are **100% synthetic demonstration records**. They do not represent real individuals, actual law enforcement cases, or live enterprise security incidents.
2. **Concurrent Multi-User Locking:** Since data persistence relies on direct file I/O on local CSV files via Pandas, the system is designed for single-evaluator / local academic demonstration. For production deployment with thousands of concurrent users, a transactional SQL/NoSQL engine would be adopted.
3. **No External Network Dependencies:** The application requires no internet access once Python packages are installed; it runs completely offline.
