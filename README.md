# 📊 Customer Churn Prediction & Retention Intelligence System

> An end-to-end Machine Learning Web Application & REST API that predicts telecom customer churn risk in real-time and prescribes automated, data-driven retention action plans.

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
└───────────────────────────┴────────────────────────────┘
```

---

## 🎯 Problem Statement

Customer churn is one of the most expensive challenges in the telecommunications and subscription industry. Acquiring a new customer costs **5–7× more** than retaining an existing one. Yet most companies only react *after* a customer has already canceled their service.

This system solves two core problems:
1. **Predict Churn Risk**: Accurately estimates each customer's likelihood of leaving using a trained Machine Learning model.
2. **Prescribe Retention Actions**: Automatically generates tailored retention offers and strategies *before* the customer cancels, based on empirical exploratory data analysis (EDA) insights.

---

## 💡 Key Features

- ⚡ **Real-Time Predictions**: Calculates instant churn probabilities and classifies customers into **LOW (0–30%)**, **MEDIUM (30–60%)**, and **HIGH (60–100%)** risk tiers.
- 🧠 **Retention Intelligence Engine**: Diagnoses customer risk drivers (e.g., month-to-month contracts, fiber optic pricing sensitivity, lack of tech support) and prescribes top 3 actionable retention steps.
- 🎨 **Modern Dark-Mode Interface**: High-contrast glassmorphism aesthetic, accessible high-contrast form controls, animated progress bars, and reactive total charges calculation.
- 🔌 **REST API Ready**: Dedicated `POST /predict` JSON API endpoint for integration into external CRM systems, dashboards, or automated marketing workflows.
- 🚀 **Production-Grade Deployment**: Pre-configured with `Procfile` and `Gunicorn` WSGI server for zero-downtime hosting on **Render.com**, **Railway**, or any standard cloud VPS.

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
| **Machine Learning** | Scikit-learn (Random Forest, StandardScaler), Joblib, Pandas, NumPy |
| **Frontend UI** | HTML5, Vanilla CSS3 (Custom Glassmorphism, CSS Variables), JavaScript (Fetch API) |
| **Typography & Styling** | Google Fonts (Inter), Modern Status Badges |
| **Deployment & DevOps** | Render.com, Git, Procfile |

---

## 📁 Project Structure

```
Customer-Churn-Prediction-Retention-Intelligence-System/
├── server.py                   # Production Flask application & REST API
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
├── requirements.txt            # Python dependencies (Flask, Gunicorn, ML libraries)
├── Procfile                    # Deployment process configuration for Render/Railway
├── app.py                      # Legacy Streamlit app (kept for historical reference)
└── README.md                   # Project documentation
```

---

## 🌐 Step-by-Step Cloud Deployment on Render.com

Follow these steps to deploy your live web application on **Render.com** (Free Tier):

### Step 1: Ensure Your Code is Pushed to GitHub
Make sure all your latest files (`server.py`, `Procfile`, `requirements.txt`, `templates/`, `static/`, `.pkl` models) are committed and pushed to your GitHub repository:
```bash
git add .
git commit -m "chore: prepare repository for Render deployment"
git push origin main
```

---

### Step 2: Sign in to Render
1. Visit **[https://render.com](https://render.com)**.
2. Click **Get Started** or **Sign In** and authenticate with your **GitHub account** (this makes importing repositories seamless).

---

### Step 3: Create a New Web Service
1. In the Render Dashboard, click the **New +** button in the top navigation bar.
2. Select **Web Service**.
3. Under **Connect a repository**, find and select your repository:
   `saicharan-r02/Customer-Churn-Prediction-Retention-Intelligence-System` (or your repository name).
4. Click **Connect**.

---

### Step 4: Configure Web Service Settings
Fill in the deployment configuration with the following values:

| Field | Configuration Value |
|---|---|
| **Name** | `customer-churn-prediction` *(or any unique name)* |
| **Language / Runtime** | `Python 3` |
| **Branch** | `main` |
| **Region** | Select the region closest to you (e.g. *Singapore*, *Frankfurt*, *Oregon*) |
| **Root Directory** | *(Leave blank)* |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn server:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120` |
| **Instance Type** | **Free** ($0 / month) |

---

### Step 5: Deploy the Service
1. Click **Deploy Web Service** at the bottom of the page.
2. Render will automatically:
   - Clone your repository.
   - Install dependencies from `requirements.txt`.
   - Start the Gunicorn server using `server.py`.
3. Once the build logs show `[START] Server running` and the status badge changes to **Live**, your public web address will be visible at the top:
   ```
   https://customer-churn-prediction-xxxx.onrender.com
   ```
4. Open the link in your browser to interact with the live application!

> [!NOTE]
> On Render's Free tier, instances spin down after 15 minutes of inactivity. When a new request arrives, it may take 20–30 seconds for the initial cold start.

---

## 🚀 How to Run Locally

### 1. Clone the Repository
```bash
git clone https://github.com/saicharan-r02/Customer-Churn-Prediction-Retention-Intelligence-System.git
cd Customer-Churn-Prediction-Retention-Intelligence-System
```

### 2. Install Required Dependencies
```bash
pip install -r requirements.txt
```

### 3. Start the Flask Server
```bash
python server.py
```

### 4. Open in Your Browser
Navigate to **`http://localhost:5000`** in your browser.

---

## 📡 REST API Documentation

You can query the machine learning model programmatically via HTTP requests:

### Endpoint: `POST /predict`
- **Headers**: `Content-Type: application/json`

#### Request Payload Example:
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

#### JSON Response (HTTP 200):
```json
{
  "probability": 56.0,
  "risk_level": "MEDIUM",
  "risk_factors": [
    "Month-to-month contract — these customers have a 43% churn rate vs only 3% for 2-year contracts",
    "Fiber optic subscriber — churns 2× more than DSL users (likely due to higher cost and more competition)",
    "Electronic check payment — highest churn rate among all payment methods, linked to manual payment friction"
  ],
  "actions": [
    {
      "title": "🔒 Offer contract upgrade",
      "desc": "Propose a 1-year contract with 15% monthly discount or a 2-year contract with 25% discount"
    },
    {
      "title": "🛡️ Free security bundle",
      "desc": "Add Online Security + Device Protection free for 3 months — increases service stickiness"
    },
    {
      "title": "💳 Auto-pay discount",
      "desc": "Offer a 5% monthly bill discount for switching to bank transfer or credit card auto-pay"
    }
  ]
}
```

---

## 👨‍💻 Author

Developed by **Sai Charan** — End-to-end Machine Learning, Backend Engineering & Retention Intelligence System.
