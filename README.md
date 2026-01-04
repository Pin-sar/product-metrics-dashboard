# Product Metrics & Engagement Analytics Dashboard

## Overview
This project demonstrates an **end-to-end product analytics workflow** similar to what data teams build at modern software companies. Starting from raw, event-level interaction logs, the project constructs **foundational product metrics** and visualizes them using a clean, executive-friendly **Power BI dashboard**.

The work focuses on:
- Correct **metric definition and aggregation**
- Time-aware analysis using **date-range controls**
- Clear communication of insights to **non-technical stakeholders**
- Dashboard design aligned with **real product decision-making**

The dataset and metrics are inspired by collaborative design and productivity tools.

---

## Repository Structure
product-metrics-dashboard/
│
├── data/
│   ├── raw_events.csv
│   ├── users.csv
│   └── sessions.csv
│
├── outputs/
│   ├── clean_events.csv
│   ├── daily_dau.csv
│   ├── daily_feature_users.csv
│   ├── sessions_per_user_day.csv
│   └── events_per_session.csv
│
├── notebooks/
│   ├── 01_generate_events.py
│   ├── 02_clean_events.py
│   ├── 03_build_metrics.py
│   └── 04_quick_charts.py
│
├── screenshots/
│   ├── dashboard_overview.png
│   └── dau_feature_zoom.png
│
├── .gitignore
└── README.md

---

## Data Model & Assumptions

The dataset is **synthetically generated** to resemble real production analytics data:

- Users interact through sessions across multiple days
- Events represent meaningful product actions (editing, commenting, exporting, etc.)
- Feature usage is mapped from low-level events to logical product capabilities
- Event timestamps and session lengths follow realistic, non-uniform distributions

This mirrors how internal analytics teams often prototype and validate metrics safely.

---

## Core Metrics

### Daily Active Users (DAU)
**Definition:**  
Number of distinct users who perform at least one tracked event on a given day.

**Implementation details:**
- Non-additive metric
- Displayed using `MAX(DAU)` per day to avoid double counting
- Serves as the primary indicator of overall product health

---

### Feature Adoption
**Definition:**  
Number of unique users interacting with each feature over a **selected time window**.

**Implementation details:**
- Aggregated using `SUM(unique_users)`
- Controlled via a date-range slicer
- Enables comparison of relative feature usage without inflating long-term totals

---

### Sessions per User
**Definition:**  
Distribution of how many sessions users initiate within a day.

**Why it matters:**
- Captures engagement depth beyond surface-level activity
- Helps differentiate casual users from power users

---

## Dashboard Design (Power BI)

The Power BI dashboard is intentionally minimal and product-oriented. It includes:

- **DAU time-series** for trend monitoring  
- **Latest DAU KPI card** for instant health checks  
- **Feature adoption bar chart** with time filtering  
- 🎚 **Date range slicer** for flexible analysis  
- **Sessions per user distribution** for engagement depth  

Design choices prioritize **clarity, interpretability, and executive usability**, following common industry standards.

---

## Example Insights

- Daily Active Users trend upward over time, indicating increasing engagement.
- A small subset of core features accounts for the majority of user interactions, consistent with Pareto-style usage patterns.
- Collaboration-related actions are associated with higher session counts, suggesting deeper engagement.
- A visible drop on the most recent date reflects **partial-day data**, a common real-world analytics consideration.

---

## How to Run

```bash
python notebooks/01_generate_events.py
python notebooks/02_clean_events.py
python notebooks/03_build_metrics.py
python notebooks/04_quick_charts.py


The generated CSVs in outputs/ can be loaded directly into Power BI Desktop to recreate the dashboard.

Why This Project Is Relevant

This project reflects how product analytics teams:

Transform raw event logs into decision-ready metrics

Avoid common aggregation pitfalls

Design dashboards that support real product discussions

Balance technical rigor with stakeholder communication

It closely mirrors analytics work performed in product, growth, and platform teams at large technology companies.

Extensions & Future Work

Funnel analysis (onboarding → activation → retention)

Cohort-based retention analysis

A/B experiment simulation and metric evaluation

Behavioral segmentation of power vs casual users

Note

All data in this repository is synthetic and generated solely for demonstration and learning purposes.


