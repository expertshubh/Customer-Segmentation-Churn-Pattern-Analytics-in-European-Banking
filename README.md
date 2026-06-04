# 🏦 Customer Segmentation & Churn Pattern Analytics
### European Banking — Data Analytics Project

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red?style=flat-square&logo=streamlit)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?style=flat-square&logo=pandas)
![Plotly](https://img.shields.io/badge/Plotly-Interactive%20Charts-3F4F75?style=flat-square&logo=plotly)
![Status](https://img.shields.io/badge/Status-Live-brightgreen?style=flat-square)

---

## 📌 Project Overview

A segmentation-driven churn analytics platform for a European retail bank operating across **France, Germany, and Spain**. The dashboard enables data-driven identification of high-risk customer groups across geography, demographics, and financial profile — turning raw data into targeted retention strategies.

> **Key Finding:** Germany's 46–60 age group churns at **67.3%** — more than 3× the European average of 20.4%.

---

## 🎯 Problem Statement

Despite having rich customer-level data, banks frequently struggle to translate raw information into targeted retention actions. Generic churn strategies fail because churn behaves differently across segments. This project addresses three core gaps:

- Which customer groups are **most at risk** of churning?
- How does churn differ across **geographies, age groups, and financial profiles**?
- What is the **revenue exposure** from high-value customer exits?

---

## 📊 Live Dashboard

> 🔗 **[Launch App on Streamlit Cloud](#)** ← *(add your deployed link here)*

**Dashboard Features:**
- 5 live KPI metric cards
- Geography × Age interaction heatmap
- High-value customer churn explorer
- Salary vs balance churn patterns
- Drill-down filters (Country, Gender, Age Group, Balance Segment)
- Revenue risk table for churned customers

---

## 🔑 Key Findings

| Segment | Churn Rate | Insight |
|---|---|---|
| **Overall** | 20.4% | 1 in 5 customers exiting |
| **Germany** | 32.4% | 2× the European average |
| **Age 46–60** | 51.1% | Majority are churning |
| **Germany × Age 46–60** | 67.3% | Highest risk segment |
| **Female customers** | 25.1% | vs 16.5% for male |
| **Inactive members** | 26.9% | vs 14.3% for active |

---

## 📐 5 KPI Metrics

| KPI | Value |
|---|---|
| Overall Churn Rate | 20.4% |
| High-Value Churn Ratio | 23.9% |
| Geographic Risk Index | 32.4% (Germany) |
| Segment Churn Rate | Up to 67.3% |
| Engagement Drop Indicator | +12.6% (Inactive vs Active) |

---

## 🗂️ Project Structure

```
├── app.py                  # Streamlit dashboard (main app)
├── analysis.py             # EDA and segmentation analysis
├── requirements.txt        # Python dependencies
├── data/
│   └── churn.csv           # European bank customer dataset (10,000 records)
```

---

## ⚙️ Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/expertshubh/Customer-Segmentation-Churn-Pattern-Analytics-in-European-Banking.git

# 2. Navigate into the project folder
cd Customer-Segmentation-Churn-Pattern-Analytics-in-European-Banking

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the dashboard
streamlit run app.py
```

Open your browser at `http://localhost:8501`

---

## 🧰 Tech Stack

| Category | Tools |
|---|---|
| Language | Python 3.10+ |
| Data Analysis | Pandas, NumPy |
| Visualisation | Plotly, Seaborn |
| Dashboard | Streamlit |
| ML / Segmentation | Scikit-learn |

---

## 📋 Dataset

- **Source:** European Bank Customer Dataset (Kaggle)
- **Records:** 10,000 customers
- **Countries:** France, Germany, Spain
- **Target Variable:** `Exited` (1 = churned, 0 = retained)
- **Features:** Credit score, geography, gender, age, tenure, balance, number of products, credit card ownership, activity status, estimated salary

---

## 💡 Strategic Recommendations

1. **Germany Retention Campaign** — 32.4% churn demands immediate country-specific intervention
2. **Middle-Aged Customer Engagement** — 46–60 age group needs tailored financial products (retirement planning, wealth management)
3. **Female Customer Retention** — 8.6% gender gap requires targeted product development
4. **Re-activate Inactive Members** — Automated re-engagement for accounts inactive 6+ months

---

## 📄 Deliverables

- ✅ Interactive Streamlit Dashboard
- ✅ EDA & Segmentation Analysis (`analysis.py`)
- ✅ Research Paper (submitted to European Central Bank)
- ✅ Executive Summary for Government Stakeholders

---

## 👤 Author

**Shubham Makvana** — Data Analyst | Python | Machine Learning | Streamlit

[![GitHub](https://img.shields.io/badge/GitHub-expertshubh-black?style=flat-square&logo=github)](https://github.com/expertshubh)

---

*Data Source: European Bank Customer Dataset | Analytics Project 2025–2026*
