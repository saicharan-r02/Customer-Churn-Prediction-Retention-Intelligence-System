# 📊 Customer Churn Prediction & Retention Intelligence System

> An end-to-end Machine Learning Web Application, REST API & CRM Database System that predicts telecom customer churn risk in real-time and prescribes automated, data-driven retention action plans.

🔴 **Live Demo**: [Click here to try the Live App](https://customer-churn-prediction-retention-sh3p.onrender.com/)

---

## 🌟 Architecture & System Design

```
┌────────────────────────────────────────────────────────┐
│               Modern Dark-Themed Web UI                │
│    (HTML5 + Vanilla CSS Glassmorphism + Responsive)    │
└───────────────────────────┬────────────────────────────┘
                            │ JSON POST /predict
                            ▼
┌────────────────────────────────────────────────────────┐
│                   Flask REST Server                    │
│             (Production WSGI with Gunicorn)            │
├───────────────────────────┬────────────────────────────┤
│   ML Inference Engine     │  Retention Intelligence    │
│  - StandardScaler         │  - Contract Upgrades       │
│  - Random Forest (80.4%)  │  - Service Bundles         │
│  - Churn Probability &    │  - Discount Offers         │
│    Risk Level (Low/Med/Hi)│  - Senior Support Plans    │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│           SQLite / SQLCipher Database Layer            │
│         (SQLAlchemy 2.0 ORM - churn_intelligence.db)   │
├────────────────────────────────────────────────────────┤
│ • customers: Demographics, billing & contracts         │
│ • churn_predictions: Timestamped risk scores & audit   │
│ • retention_outcomes: Closed-loop campaign feedback    │
└────────────────────────────────────────────────────────┘
```

---

## 🎯 Problem Statement

Customer churn is one of the most expensive challenges in the telecommunications and subscription industry. Acquiring a new customer costs **5–7× more** than retaining an existing one. Yet most companies only react *after* a customer has already canceled their service.

This system solves three core problems:
1. **Predict Churn Risk**: Accurately estimates each customer's likelihood of leaving using a trained Machine Learning model.
2. **Prescribe Retention Actions**: Automatically generates tailored retention offers and strategies *before* the customer cancels, based on empirical exploratory data analysis (EDA) insights.
3. **Persist CRM & Campaign Audit Logs**: Automatically saves predictions into a database and tracks whether retention offers were **ACCEPTED** or **DECLINED** to close the intelligence loop.

---

## 💡 Key Features

- ⚡ **Real-Time Predictions**: Calculates instant churn probabilities and classifies customers into **LOW (0–30%)**, **MEDIUM (30–60%)**, and **HIGH (60–100%)** risk tiers.
- 🧠 **Retention Intelligence Engine**: Diagnoses customer risk drivers (e.g., month-to-month contracts, fiber optic pricing sensitivity, lack of tech support) and prescribes top 3 actionable retention steps.
- 🗄️ **Persistent Database Layer (SQLite / SQLAlchemy)**: Persists customer profiles, timestamped inference results, and retention feedback with zero server maintenance.
- 🎨 **Modern Dark-Mode Interface**: High-contrast glassmorphism aesthetic, accessible high-contrast form controls, animated progress bars, and reactive total charges calculation.
- 🔌 **REST API Ready**: Dedicated endpoints (`/predict`, `/api/history`, `/api/analytics`, `/api/retention/feedback`) for integration into external CRM systems.
- 🚀 **Production-Grade Deployment**: Pre-configured with `Procfile` and `Gunicorn` WSGI server for hosting on **Render.com**, **Railway**, or cloud VPS.

---

## 🏆 Model Benchmark & Performance

Trained on **7,032 real Telco customer records** (cleaned from 7,043 rows):

| Model | Accuracy | ROC-AUC | Status |
|---|---|---|---|
| Logistic Regression | 79.3% | 0.830 | Evaluated Baseline |
| **Random Forest Classifier** | **80.4%** | **0.850** | **✅ Selected for Production** |
| Gradient Boosting | 80.1% | 0.845 | Evaluated |

**Selected Model**: **Random Forest** achieved the highest ROC-AUC score (**0.850**) and best generalization across demographic and service feature spaces.

---

## 📊 Key Data Insights & Retention Rules

| Feature / Pattern | Data Finding | Actionable Retention Rule |
|---|---|---|
| **Month-to-Month Contracts** | **43% churn rate** vs only 3% for 2-year contracts | Offer contract upgrade with 15–25% discount |
| **Early Tenure (< 12 mos)** | **68% of all churn** occurs in the first year | Assign dedicated account manager + milestone loyalty gift |
| **Fiber Optic Internet** | Churns **2× more** than DSL (cost & competition) | Bundle free security / device protection for 3 months |
| **Electronic Check Payments** | Highest churn rate among all payment methods | Provide 5% recurring discount for switching to auto-pay |
| **Seniors without Tech Support** | High risk of passive churn from service friction | Provide complimentary tech support + priority customer line |

---

## 🛠️ Tech Stack

| Layer | Technologies |
|---|---|
| **Backend & Server** | Python 3, Flask, Gunicorn (WSGI) |
| **Database & ORM** | SQLite / SQLCipher, SQLAlchemy 2.0 (`churn_intelligence.db`) |
| **Machine Learning** | Scikit-learn (Random Forest, StandardScaler), Joblib, Pandas, NumPy |
| **Frontend UI** | HTML5, Vanilla CSS3 (Custom Glassmorphism, CSS Variables), JavaScript (Fetch API) |
| **Deployment & DevOps** | Render.com, Git, Procfile |

---

## 📁 Project Structure

```
Customer-Churn-Prediction-Retention-Intelligence-System/
├── database.py                 # SQLAlchemy ORM models, session & CRM queries
├── server.py                   # Production Flask application & REST API
├── churn_intelligence.db       # SQLite database (auto-created on startup)
├── templates/
│   └── index.html              # Frontend user interface template
├── static/
│   └── style.css               # Modern dark-theme glassmorphism stylesheet
├── columns.json                # Expected feature column schema for inference
├── rf_model.pkl                # Production Random Forest ML model artifact
├── scaler.pkl                  # Fitted StandardScaler artifact
├── lr_model.pkl                # Baseline Logistic Regression model
├── Customer_Churn_Project.ipynb# EDA, feature engineering & model training notebook
├── Customer-Churn.csv          # Telco customer dataset
├── requirements.txt            # Python dependencies (Flask, SQLAlchemy, Gunicorn, ML)
├── Procfile                    # Deployment process configuration for Render/Railway
├── app.py                      # Legacy Streamlit app (kept for reference)
└── README.md                   # Project documentation
```

---

## 🗃️ Database Schema & Inspection

The system utilizes an embedded **SQLite / SQLCipher** database ([`churn_intelligence.db`](file:///c:/Users/saich/OneDrive/Desktop/python/Customer-Churn-Prediction-Retention-Intelligence-System/churn_intelligence.db)):

### Database Tables:
1. `customers`: Stores demographics (`gender`, `senior_citizen`, `partner`, `dependents`), contract type, payment method, tenure, and billing.
2. `churn_predictions`: Stores every ML prediction (`churn_probability`, `risk_level`, `risk_factors`, `predicted_at`).
3. `retention_outcomes`: Tracks action taken, customer response (`PENDING`, `ACCEPTED`, `DECLINED`), and notes.

### How to Check / Query Stored Data:
Run this Python one-liner in your terminal:
```bash
python -c "
import sqlite3, pandas as pd
conn = sqlite3.connect('churn_intelligence.db')
print('=== RECENT PREDICTIONS AUDIT LOG ===')
print(pd.read_sql_query('SELECT * FROM churn_predictions ORDER BY predicted_at DESC LIMIT 5;', conn))
print('\n=== RETENTION CAMPAIGN OUTCOMES ===')
print(pd.read_sql_query('SELECT * FROM retention_outcomes LIMIT 5;', conn))
"
```
Or open `churn_intelligence.db` in **DB Browser for SQLite** or **VS Code SQLite Viewer**.

---

## 📡 REST API Documentation

### 1. `POST /predict` — Run ML Inference & Save Audit Log
* **Payload**:
```json
{
  "tenure": 12,
  "monthly_charges": 75.50,
  "total_charges": 906.00,
  "gender": "Female",
  "senior": "No",
  "partner": "Yes",
  "dependents": "No",
  "phone": "Yes",
  "multiple_lines": "No",
  "internet": "Fiber optic",
  "online_security": "No",
  "online_backup": "No",
  "device_protection": "Yes",
  "tech_support": "No",
  "streaming_tv": "Yes",
  "streaming_movies": "No",
  "paperless": "Yes",
  "contract": "Month-to-month",
  "payment": "Electronic check"
}
```
* **Response (HTTP 200)**:
```json
{
  "prediction_id": 1,
  "probability": 56.0,
  "risk_level": "MEDIUM",
  "risk_factors": ["Month-to-month contract...", "Fiber optic subscriber..."],
  "actions": [{"title": "🔒 Offer contract upgrade", "desc": "Propose 1-year contract..."}]
}
```

### 2. `GET /api/history` — Get Recent Audit Log
Returns the latest predictions, associated customer metadata, and current retention campaign status.

### 3. `GET /api/analytics` — Executive Churn Metrics
Returns total predictions, average predicted churn probability, risk tier distribution (`LOW`, `MEDIUM`, `HIGH`), and retention acceptance rates.

### 4. `POST /api/retention/feedback` — Log Retention Campaign Outcome
* **Payload**:
```json
{
  "prediction_id": 1,
  "status": "ACCEPTED",
  "action_taken": "Applied 15% 1-Year Promotion",
  "notes": "Customer agreed to 1-year contract renewal"
}
```

---

## 🚀 How to Run Locally

### 1. Clone & Install Dependencies
```bash
git clone https://github.com/saicharan-r02/Customer-Churn-Prediction-Retention-Intelligence-System.git
cd Customer-Churn-Prediction-Retention-Intelligence-System
pip install -r requirements.txt
```

### 2. Start the Server
```bash
python server.py
```
Open **`http://localhost:5000`** in your browser.

---

## 👨‍💻 Author

Developed by **Sai Charan** — End-to-end Machine Learning, Backend Engineering & Retention Intelligence System.
