# 🚧 FleetOps AI — Intelligent Operations Agent for Heavy Machinery

[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-FF4B4B.svg?style=flat&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Machine Learning](https://img.shields.io/badge/ML-Isolation%20Forest-orange.svg?style=flat&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Track](https://img.shields.io/badge/Track-AI%20%2B%20Construction%20Machinery-darkgreen.svg?style=flat)](#)

> **China International College Students' Innovation & Entrepreneurship Competition**  
> *Track: AI + Construction Machinery → AI + Operations*

---

## 📌 Executive Summary

**FleetOps AI** turns raw, low-level equipment operational logs (operating hours, downtime, fuel consumption, and maintenance flags) into **actionable, prioritized operational decisions**. Instead of requiring fleet managers to manually sift through dense spreadsheets, FleetOps AI classifies and ranks fleet equipment based on operational urgency using a unified **Attention Score (0–100)**.

In addition to interactive dashboard analytics, FleetOps AI features a natural-language **AI Agent** capable of answering complex operational queries ("Which equipment needs urgent maintenance?", "What is driving the fuel cost spike?").

---

## ✨ Key Features

1. **📊 Operational Overview & Analytics:**
   - Real-time fleet health KPIs (Fleet Size, Overall Utilization %, Operating Hours, Total Fuel Consumption).
   - Equipment downtime rankings & utilization rate breakdown by construction project.

2. **🎯 Unified Priority Ranking (Attention Score 0–100):**
   Combines four multi-dimensional operational signals:
   - **Downtime Rate:** Excessive idle time vs. operating hours.
   - **Fuel Deviation:** Consumption relative to the equipment type baseline.
   - **Maintenance Frequency:** High breakdown and service intervals.
   - **Unsupervised Anomaly Detection:** Outlier detection via `Isolation Forest`.

3. **💬 Natural-Language AI Agent:**
   - Multi-mode engine: Runs in **Real Mode** using OpenAI Function Calling or **Test Mode** (rule-based engine without requiring API keys).

4. **📂 Custom Dataset Benchmark & Upload:**
   - Supports custom CSV uploads (`equipment_master.csv` & `fleet_daily_logs.csv`) to test external fleet datasets on the exact same analytics pipeline.

---

## 🛠️ Tech Stack & Architecture

- **Frontend / Dashboard UI:** Streamlit (Custom XCMG-inspired Industrial Theme CSS)
- **Data Processing & Analytics:** Pandas, NumPy
- **Visualizations:** Plotly Express & Plotly Graph Objects
- **Machine Learning:** Scikit-Learn (Isolation Forest for Anomaly Detection)
- **LLM Integration:** OpenAI GPT API with structured function calling

---

## 📁 Repository Structure

```text
fleetops-ai/
├── app/
│   └── main.py                     # Streamlit application entry point
├── src/
│   ├── agent.py                    # Natural language agent logic & LLM router
│   ├── tools.py                    # Fleet reporting & analytics engines
│   ├── ml_anomaly.py               # Isolation Forest & Attention Score calculation
│   └── generate_data.py            # Synthetic fleet log generator
├── data/
│   ├── equipment_master.csv        # Equipment metadata
│   └── fleet_daily_logs.csv        # Daily telemetry logs
├── requirements.txt                # Python dependencies
└── README.md                       # Project documentation
