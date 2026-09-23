# FleetOps AI — AI Operations Agent for Construction Equipment

> **Turning fleet data into operational decisions.**
>
> FleetOps AI is an AI-powered operations dashboard and agent designed for construction machinery. It transforms equipment data — including **operating hours, downtime, fuel consumption, maintenance, utilization, and anomalies** — into clear KPIs, actionable insights, and natural-language answers.

**Track:** AI + Construction Machinery → AI + Operations  
**Competition:** 15th China International College Students' Innovation & Entrepreneurship Competition  
**Built by:** Raghad Altrisy • Taif Alharbi • Jood Alwajeeh

---

## 🚜 What is FleetOps AI?

Construction fleets generate a large amount of operational data, but raw numbers do not automatically tell managers **what needs attention, why it matters, or what to do next**.

FleetOps AI bridges that gap with four connected capabilities:

- 📊 **Live Fleet Dashboard** — monitor KPIs, downtime, utilization, and equipment attention levels.
- 🤖 **AI Operations Agent** — ask operational questions in natural language and receive analytical answers.
- 🧠 **Machine Learning** — detect unusual equipment behavior using Isolation Forest and combine signals into a unified Attention Score.
- 📋 **Manager-ready Reports** — turn fleet analytics into downloadable CSV, JSON, and PDF reports.

The result is a prototype designed around a simple operational workflow:

**Monitor → Understand → Detect → Recommend → Act**

---

## ✨ Key Features

### 📊 Interactive Fleet Dashboard

The Streamlit dashboard provides a single view of fleet performance, including:

- Fleet-level KPI cards
- Equipment downtime analysis
- Project utilization analysis
- Unified Attention Score rankings
- AI-powered fleet insights
- What-if downtime simulation
- Maintenance planning
- Data upload and analysis

### 🎨 Clear, Theme-Aware Visualizations

Charts were designed to remain readable in both **Light Mode and Dark Mode**.

- **Downtime chart:** continuous low-to-high warning gradient driven by the actual `downtime_rate_%` values.
- **Utilization chart:** continuous performance gradient across projects.
- Clear chart titles, axis labels, tick labels, grids, and annotations.
- Theme-aware chart styling for improved readability.
- **Chart Appearance** can be set to `Auto`, `Light`, or `Dark` from the Sidebar.
- Optional value labels can be enabled or disabled.

This makes the dashboard suitable for both normal viewing and presentation/demo environments.

### ⚙️ Configurable Sidebar

The Sidebar exposes practical dashboard controls instead of hiding them inside the code:

- **AI Mode** — Built-in/Test Mode or Real/OpenAI API Mode
- **Top-N chart items** — control how many equipment items are displayed
- **Downtime chart scale** — adjust the visualization range
- **Show chart values** — toggle value labels
- **Chart appearance** — Auto / Light / Dark
- **Reset data** — restore the default dataset
- **Refresh controls** — refresh the dashboard state

### 🤖 AI Operations Agent

Users can ask questions such as:

- *Which equipment has the highest downtime?*
- *Which machines need immediate attention?*
- *Why is utilization declining in this project?*
- *Is there an unusual fuel-consumption pattern?*
- *Give me a fleet performance report.*

The agent maps questions to analytical tools and returns operationally useful results rather than simply exposing raw data.

### 🔌 Two AI Modes

#### Built-in AI Mode — No API Key Required

A local routing and analytics layer combines:

- Intent routing
- KPI analysis
- Rule-based operational logic
- Machine Learning anomaly detection
- Fleet reporting tools

This makes the project demonstrable even without an external LLM API key.

#### Real LLM Mode — OpenAI API

When `OPENAI_API_KEY` is available, the agent can use:

- OpenAI Chat Completions
- Function Calling
- The same underlying fleet-analysis tools

This provides a natural-language interface on top of the project's analytical layer.

---

## 🧠 Analytics & Machine Learning

FleetOps AI combines traditional analytics with ML-based anomaly detection.

### Core KPIs

The pipeline calculates operational indicators including:

- Operating hours
- Downtime
- Downtime rate
- Fuel consumption
- Utilization
- Maintenance-related signals
- Equipment-level attention indicators

### Isolation Forest

The project uses **Isolation Forest** to identify unusual operational behavior, particularly for fuel-consumption anomalies.

### Unified Attention Score

Instead of looking at a single metric in isolation, FleetOps combines relevant warning signals into a unified **Attention Score** to help identify equipment that may require further investigation.

The dashboard then connects the score to **reasons and recommended actions**, making the output more useful for operational decision-making.

---

## 🛠️ Analysis Tool Functions

The AI Agent is backed by modular analytical tools:

| Tool | Purpose |
|---|---|
| `get_top_downtime_equipment(top_n)` | Identifies equipment with the highest downtime |
| `get_equipment_needing_attention(threshold)` | Finds equipment requiring attention using downtime and maintenance/anomaly signals, compared within equipment type |
| `explain_utilization_trend(project)` | Analyzes a project's utilization trend and its likely contributing factors |
| `analyze_fuel_consumption(equipment_id)` | Detects recent fuel-consumption spikes and anomalies |
| `generate_fleet_report()` | Generates a comprehensive fleet performance report |

The modular design allows the analytical tools to be reused by both the Built-in AI Mode and the LLM-powered agent.

---

## 📋 Reporting & Export

The **Report** tab converts the current fleet analysis into downloadable formats:

- 📊 **CSV** — convenient for further analysis in Excel, Power BI, or other tools.
- 🔗 **JSON** — structured output for applications and integrations.
- 📄 **PDF** — manager-friendly fleet performance report.

The report includes operational findings and **recommended manager actions**, turning analytics into a decision-support artifact.

---

## 🔮 What-If & Maintenance Planning

FleetOps AI goes beyond monitoring by supporting operational exploration.

### What-If Simulator

Users can explore the effect of changing downtime assumptions and compare the resulting scenario against the current fleet situation.

### Maintenance Planner

The maintenance workflow helps surface equipment that deserves attention and connects the analysis to recommended next steps.

These capabilities demonstrate how the system can move from **descriptive analytics** toward **decision support**.

---

## 📦 Dataset

The prototype uses a synthetic operational dataset representing:

- **30 construction machines**
- **90 days** of daily operational records
- **5 construction projects**
- Equipment types including:
  - Excavators
  - Loaders
  - Dump Trucks
  - Bulldozers
  - Cranes
  - Graders

The dataset intentionally contains realistic operational patterns and demonstration scenarios:

- 3 machines with unusually high downtime
- 1 machine with a sudden fuel-consumption increase during the final 20 days
- 1 project with a gradual utilization decline

> **Important:** The dataset is synthetic and is used for prototype/demo purposes. The pipeline is structured so that real operational data can replace it when data with the same required fields becomes available.

---

## 🏗️ Project Architecture

```text
fleetops-ai/
├── data/                       # Raw and processed fleet data
│   ├── equipment_master.csv
│   ├── fleet_daily_logs.csv
│   ├── equipment_kpis.csv
│   └── weekly_utilization_by_project.csv
│
├── notebooks/                  # EDA and analysis
│   └── FleetOps_EDA.ipynb
│
├── src/                        # Core analytics, AI, ML, and generation
│   ├── agent.py
│   ├── tools.py
│   ├── generate_data.py
│   ├── kpis.py
│   ├── ml_anomaly.py
│   ├── test_suite.py
│   └── ...
│
├── app/                        # Streamlit application
│   └── main.py
│
├── reports/                    # Project and test reports
│   ├── FleetOps_AI_Project_Report.pdf
│   ├── FleetOps_AI_Test_Report.pdf
│   └── test_results.json
│
├── presentation/               # Presentation and demo materials
│   ├── FleetOps_AI_Presentation.pptx
│   └── Demo_Video_Script.md
│
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Generate the synthetic dataset

```bash
python src/generate_data.py
```

### 3. Calculate KPIs

```bash
python src/kpis.py
```

### 4. Launch the Streamlit dashboard

```bash
streamlit run app/main.py
```

The dashboard can then be used for fleet monitoring, AI questions, anomaly analysis, what-if simulation, maintenance planning, and report export.

---

## 🔐 Optional: Enable Real LLM Mode

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=sk-...
```

Then run the agent/application normally. When the API key is available, the project can use the LLM-powered mode with Function Calling.

> Never commit your real API key to GitHub. Add `.env` to `.gitignore` before publishing the repository.

---

## 🧪 Reliability & Testing

Reliability was treated as part of the product rather than an afterthought.

The project includes edge-case testing covering ambiguous, empty, and invalid inputs. The final test report records **16/16 successful tests**.

The agent also includes safeguards for common failure cases:

- Explicit **Top-N** requests are respected — e.g. Top 3 returns exactly 3 results.
- Named **project filters** are preserved in utilization questions.
- Equipment IDs are validated instead of silently falling back to another unit.
- Maintenance and Attention Score results include a **reason + recommended action**.
- Fleet reports include **three manager actions**.
- Built-in AI Mode responds in **Arabic when the user asks in Arabic**.

---

## 📈 Development Progress

The project was developed through a structured 10-day progression:

| Day | Milestone | Status |
|---|---|---|
| 1–2 | Project structure + synthetic fleet dataset | ✅ Complete |
| 3 | KPI calculation | ✅ Complete |
| 4 | AI Agent analysis tools | ✅ Complete |
| 5 | LLM integration + Built-in AI Mode | ✅ Complete |
| 6 | Streamlit Dashboard + Chat | ✅ Complete |
| 7 | Isolation Forest + unified Attention Score | ✅ Complete |
| 8 | Edge-case and reliability testing | ✅ Complete |
| 9 | PDF report + PPTX + Colab/EDA materials | ✅ Complete |
| 10 | Final review and submission package | ✅ Complete |

---

## 📁 Official Deliverables

| Deliverable | Location | Status |
|---|---|---|
| Proposal / Project Report | `reports/FleetOps_AI_Project_Report.pdf` | ✅ Ready |
| Model / Application Source Code | This repository | ✅ Ready |
| Test Report | `reports/FleetOps_AI_Test_Report.pdf` | ✅ Ready |
| Test Results | `reports/test_results.json` | ✅ Ready |
| Presentation | `presentation/FleetOps_AI_Presentation.pptx` | ✅ Ready |
| Demo Video Script | `presentation/Demo_Video_Script.md` | ✅ Ready |
| EDA Notebook | `notebooks/FleetOps_EDA.ipynb` | ✅ Ready |

---

## 🎯 Why FleetOps AI?

FleetOps AI is designed around a practical operations problem: **how can a construction fleet team move from raw equipment data to a clear action?**

Instead of presenting isolated charts, the system connects:

**Data → KPIs → Anomalies → Attention Score → AI Explanation → Recommended Action → Report**

This architecture demonstrates how AI and machine learning can complement conventional fleet analytics and support more informed construction-equipment operations.

---

## 🏆 Competition Context

**15th China International College Students' Innovation & Entrepreneurship Competition**

**Track:** AI + Construction Machinery → AI + Operations

**Team:** Raghad Altrisy • Taif Alharbi • Jood Alwajeeh

**Product capabilities:** 📊 Live Dashboard • 🔌 REST API • 🤖 AI-Powered • 🚀 Production Ready

---

## 👥 Team

**Raghad Altrisy • Taif Alharbi • Jood Alwajeeh**

FleetOps AI was built as a collaborative AI + Operations prototype focused on applying data analytics, machine learning, and natural-language AI to construction machinery operations.

---

## ⚠️ Prototype Disclaimer

FleetOps AI is an academic/prototype project built for demonstration and competition purposes. The included dataset is synthetic and does not represent the operational performance of any real company, project, or equipment fleet.
