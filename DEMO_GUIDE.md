# 🎓 CIMS Project Demonstration & Viva Evaluation Guide
### Cybercrime Incident Management System (CIMS) & Analytics

> **Audience:** B.Tech Second-Year / Academic Project Evaluators  
> **Course:** Data Visualization / Cyber Security / Python Application Development  
> **Target Duration:** 8 to 12 minutes

---

## 📌 Demonstration Roadmap Summary

| Step | Section | Time | Key Takeaway |
|------|---------|------|--------------|
| **1** | Introduction & Architecture | 1 min | 100% Python/Streamlit, pure CSV data store, dark theme |
| **2** | Executive Dashboard Overview | 2 mins | Real-time KPIs, 6 Plotly charts, 2-column balanced layout |
| **3** | Dynamic Global Filtering | 2 mins | Filter by Type, Priority, Status, Location & Date; Clear button |
| **4** | Dataset Explorer, Search & CRUD | 3 mins | Instant multi-column search, Column toggle, Add/Edit/Delete, CSV download |
| **5** | Academic Analytics Pages | 3 mins | Matplotlib, Seaborn heatmaps, KDE histograms, NumPy vector math |
| **6** | Q&A & Architecture Wrap-up | 1 min | Referential integrity, audit trail, academic outcomes |

---

## 🚀 Step 1: Launch & Introduction (1 Minute)

1. Open PowerShell and start the app:
   ```powershell
   cd "c:\Users\sahas\OneDrive\Desktop\cybercrime\Cybercrime-Analytics"
   streamlit run app.py
   ```
2. Explain to the evaluator:
   > *"Good morning/afternoon, Sir/Madam. This project is the **Cybercrime Incident Management System (CIMS) & Analytics Platform**.*  
   > *It solves the problem of analyzing, prioritizing, and managing cybercrime incident dossiers, forensic evidence, and financial loss data.*  
   > *The architecture is 100% Python-based, utilizing Streamlit for the front-end, Pandas for data processing, NumPy for array calculations, and Plotly, Matplotlib, and Seaborn for multi-dimensional data visualization.*  
   > *It operates on an interconnected local CSV data store with full CRUD capabilities and complete referential integrity."*

---

## 📊 Step 2: Executive Dashboard (2 Minutes)

Point out the main landing page (`app.py`):

1. **Top KPI Cards (5 Metrics):**
   - **Total Incidents:** 12 incidents currently in the database.
   - **Total Cases:** 12 investigative case dossiers linked to incidents.
   - **Active Cases:** 7 cases requiring ongoing investigation or triage.
   - **Resolved Cases:** 5 closed/resolved cases.
   - **Total Financial Loss:** ₹11,095,000 (Average loss ~₹924,583 per incident).
2. **Explain the 6 Executive Charts (Plotly):**
   - **Row 1:**
     - *Incidents by Crime Classification (Bar Chart):* Highlights distribution (Phishing, Ransomware, Financial Fraud, etc.).
     - *Incidents by Resolution Status (Donut Chart):* Visualizes proportion of Resolved vs. Under Investigation vs. Reported vs. Pending.
   - **Row 2:**
     - *Incidents by Priority Severity (Bar Chart):* Color-coded distribution across `Critical`, `High`, `Medium`, and `Low`.
     - *Monthly Incident Inflow Trajectory (Area Chart):* Shows monthly trend peaks (e.g., spike in June).
   - **Row 3:**
     - *Total Financial Loss by Attack Vector (Bar Chart):* Displays monetary exposure in INR with currency labels. Financial Fraud (~₹3.95M) and Data Breaches (~₹2.4M) account for the highest losses.
     - *Active Investigation Cases by Status (Donut Chart):* Status of linked formal police dossiers (`Open`, `Under Investigation`, `Closed`).
3. **Responsive Layout:**
   - Emphasize that the charts are rendered in a clean 2-column grid with horizontal legends beneath the plots, ensuring **zero horizontal clipping** on any screen resolution.

---

## 🎛️ Step 3: Demonstrate Global Sidebar Filters (2 Minutes)

Demonstrate that the sidebar filters are persistent, unified, and immediately update all calculations.

1. **Test 1 — Filter by Crime Type:**
   - In the sidebar under **🎛️ Dashboard Filters**, open the **`🏷️ Incident Type`** dropdown.
   - Select **`Phishing`**.
   - **Observation:**
     - The top filter banner appears: `🔍 Filtered View: 2 of 12 incidents match criteria`.
     - Total Incidents updates to **2**.
     - Financial Loss updates to **₹525,000** (Avg: ₹262,500).
     - The charts update to reflect only Phishing cases (SMS Smishing & Email harvesting in Mumbai and Bengaluru).
2. **Test 2 — Filter by Priority:**
   - Change Priority to **`Critical`**.
   - Select Incident Type back to **`All`**.
   - **Observation:**
     - Displays 4 Critical incidents (Ransomware, Financial Fraud, Data Breach).
     - Financial loss recalculates to **₹8,150,000**.
3. **Test 3 — Location Filter:**
   - Select **`Maharashtra`** in State / Location dropdown.
   - **Observation:** Shows 4 incidents centered in Mumbai and Pune.
4. **Test 4 — One-Click Reset:**
   - Click the **`🔄 Clear All Filters`** button in the sidebar.
   - **Observation:** All dropdowns immediately return to `All`, the date range resets to the full dataset bounds, and all 12 incidents reappear.

---

## 🗂️ Step 4: Dataset Explorer, Instant Search & CRUD Lifecycle (3 Minutes)

Navigate to **`5_Dataset_Explorer`** from the sidebar.

### A. Demonstrate Multi-Column Instant Search
1. Locate the prominent search bar **`🔍 Search Incidents`**.
2. Type **`INC-2024-001`**:
   - The table immediately filters to show only the State Bank Credential Harvesting incident.
3. Clear the search and type **`Mumbai`**:
   - Instantly shows all incidents located in Mumbai.
4. Clear the search and type **`Critical`**:
   - Shows all Critical severity records across all attack types.

### B. Demonstrate Column Selection & CSV Export
1. In the **`📋 Columns to Display`** multiselect, deselect a few columns (e.g., remove `channel` and `city`).
2. Notice the table updates dynamically to only show your selected columns.
3. Click **`💾 Download Matching Incidents (CSV)`** to prove that the downloaded CSV matches the exact filtered search result.

### C. Demonstrate Full CRUD Lifecycle
Show that changes persist to the underlying CSV files and write to the audit trail:

1. **Create (Add Incident):**
   - Click to expand **`➕ Log New Incident`**.
   - Enter test values:
     - Incident ID: `INC-2024-013`
     - Crime Type: `Ransomware`
     - Loss (INR): `450000`
     - City: `Bengaluru`, State: `Karnataka`
     - Priority: `High`, Status: `Reported`
   - Click **`Record Incident`**.
   - Notice the success message, table refresh (now 13 incidents), and an audit entry recorded in the Audit Logs tab!
2. **Update (Edit Incident):**
   - Click to expand **`✏️ Update Incident Record`**.
   - Select `INC-2024-013`.
   - Change Status to **`Resolved`** and Financial Loss to **`600000`**.
   - Click **`Save Changes to CSV`**.
   - Observe the table immediately reflecting the new status and updated loss.
3. **Delete (Remove Incident):**
   - Click to expand **`🗑️ Delete Incident Record`**.
   - Select `INC-2024-013`, check the confirmation box, and click **`Delete Incident Permanently`**.
   - Notice the record is cleanly purged, restoring the dataset back to its original 12 records.
4. **Inspect Audit Trail:**
   - Switch to the **`📜 Audit Logs`** tab.
   - Point out that every single creation, edit, and deletion has been logged chronologically with timestamps and user references!

---

## 📈 Step 5: Academic Analytics Modules (3 Minutes)

Walk the evaluator through the specialized analytical pages:

### 1. Crime Analysis (`pages/1_Crime_Analysis.py`)
- **Showcase:**
  - Attack Delivery Channels donut chart.
  - State and Metropolitan City breakdown bar charts.
  - **Academic Highlight (Seaborn):** Point out the **Priority vs. Status Cross-Tabulation Heatmap** created using `pd.crosstab()` and Seaborn. Explain how it visualizes case progression by threat severity.
  - **Matplotlib static bar plot:** Demonstrates native Matplotlib figure creation with dark styling.

### 2. Trend Analysis (`pages/2_Trend_Analysis.py`)
- **Showcase:**
  - Monthly incident volume progression line chart.
  - Dynamic monthly attack-vector pivot table.
  - **Academic Highlight (NumPy):** Point out the **Moving Average Smoothed Window** line chart calculated using NumPy vector arrays (`rolling(window=2).mean()`). Explain how temporal smoothing helps identify true trends by removing daily noise.

### 3. Financial Analysis (`pages/3_Financial_Analysis.py`)
- **Showcase:**
  - Quantitative monetary damage analysis (Total, Mean, Peak).
  - **Plotly Hierarchical Treemap:** Click on state nodes (`Maharashtra` or `Karnataka`) to zoom into proportional loss breakdowns by crime vector.
  - **Academic Highlight (Seaborn & NumPy):**
    - Seaborn Boxplot showing financial loss dispersion and outliers per priority category.
    - Explicit **NumPy statistical metrics table**: Arithmetic Mean, Median, Standard Deviation, 25th & 75th percentiles, and Interquartile Range (IQR).

### 4. Statistical Analysis (`pages/4_Statistical_Analysis.py`)
- **Showcase:**
  - **Academic Highlight (Seaborn Heatmap):** Pearson Correlation Matrix between encoded metrics (Priority, Status, Loss, Month).
  - **Academic Highlight (Seaborn Histogram with KDE):** Kernel Density Estimation curve showing that financial losses follow a heavy-tailed positive skew (most incidents have moderate losses, with occasional severe outliers).
  - **Academic Highlight (NumPy Vectorization):** Point out the code snippet and live table demonstrating **Min-Max Feature Scaling** ($X_{norm} = \frac{X - X_{min}}{X_{max} - X_{min}}$).

---

## 🎯 Step 6: Expected Baseline Results for Verification

When evaluators check your default baseline dataset (all filters set to `All`):

| Metric | Expected Baseline Value |
|--------|-------------------------|
| Total Incidents | **12** |
| Total Investigation Cases | **12** |
| Active Cases (`Open` / `Under Investigation`) | **7** |
| Resolved Cases (`Closed`) | **5** |
| Total Cumulative Financial Loss | **₹11,095,000** |
| Average Loss per Incident | **₹924,583** |
| Peak Incident Loss | **₹3,100,000** (`INC-2024-011` — Financial Fraud via CFO Compromise) |
| Total Evidence Records | **10** (6 Verified, 3 Pending Review, 1 Rejected) |
| Total Registered Investigators | **4** (All Active) |
| Primary Crime Vectors | Phishing (2), Financial Fraud (2), Ransomware (1), Data Breach (1), DDoS (1), Hacking (1), Identity Theft (1), Cyberstalking (1), Social Engineering (1), Online Fraud (1) |

---

## 💡 Potential Evaluator Questions & Winning Answers

1. **Q: Why are you using local CSV files instead of MySQL?**
   - *A: "Local CSV files provide a portable, zero-configuration data layer ideal for academic evaluation and standalone offline deployment. By leveraging Pandas DataFrame indexing, our read and write operations are instantaneous in memory, while remaining completely persistent across app restarts."*
2. **Q: How did you ensure data consistency between incidents, cases, and evidence?**
   - *A: "We implemented strict referential integrity checks in our data ingestion module. Every incident maps to a unique `case_id`, every case links back to an `incident_id`, and evidence records must reference valid case identifiers and registered investigator user IDs. In addition, all CRUD operations automatically generate audit logs."*
3. **Q: How does the NumPy moving average work in Trend Analysis?**
   - *A: "We take chronological incident frequencies, extract daily count series as NumPy float arrays, and compute rolling window averages using convolution and Pandas rolling frames. This reduces stochastic variance and surfaces the underlying trend curve."*
4. **Q: How did you prevent chart clipping and horizontal overflow?**
   - *A: "We set Streamlit's container width to a fluid 98%, enabled Plotly's responsive config, shifted legends below charts horizontally, and tailored Matplotlib and Seaborn dimensions to `(6.5, 3.6)` inches with container auto-scaling."*

