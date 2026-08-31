# 📊 Customer Churn Prediction & Retention Intelligence System

> Predict which telecom customers are at risk of leaving — and get a personalised, data-driven action plan to retain them in real time.

---

## 🌟 Overview & Architecture

This project is a **production-ready Machine Learning Web Server** built with Flask, Gunicorn, and a custom modern dark-themed web interface. It combines predictive analytics with business intelligence to not only detect customer churn risk but also recommend actionable retention strategies.

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

Customer churn is one of the most costly challenges in the telecom and subscription industry. Acquiring a new customer costs **5–7× more** than retaining an existing one. Yet most companies only react after a customer has already canceled their service.

This system solves two critical problems:
1. **Predict Churn Risk**: Accurately estimates each customer's probability of leaving using machine learning.
2. **Prescribe Retention Actions**: Generates automated, tailored retention plans *before* the customer churns based on EDA data insights.

---

## 💡 Key Features

- ⚡ **Real-Time Predictions**: Instant churn score calculation and risk classification (Low, Medium, High).
- 🧠 **Retention Intelligence Engine**: Dynamic root-cause diagnosis explaining *why* the customer is at risk, paired with 3 tailored retention action items.
- 🎨 **Modern Dark-Mode UI**: Glassmorphism aesthetic, accessible high-contrast form controls, animated progress bars, and reactive charge calculations.
- 🔌 **REST API Ready**: Clean `POST /predict` JSON API endpoint for seamless integration into external CRM tools or enterprise dashboards.
- 🚀 **Cloud-Native Deployment**: Production-configured with `Procfile` and `gunicorn` for 1-click deployment to **Render.com**, **Railway**, or VPS.

---

## 🏆 Model Benchmark & Performance

Trained on **7,032 real Telco customer records** (cleaned from 7,043 rows):

| Model | Accuracy | ROC-AUC | Status |
|---|---|---|---|
| Logistic Regression | 79.3% | 0.830 | Evaluated |
| **Random Forest Classifier** | **80.4%** | **0.850** | **✅ Selected for Production** |
| Gradient Boosting | 80.1% | 0.845 | Evaluated |

**Winner**: **Random Forest** achieved the highest ROC-AUC (0.850) and best generalization across demographic and service feature spaces.

---

## 📊 Key EDA Insights

| Discovery | Data Insight | Retention Strategy |
|---|---|---|
| **Month-to-month contracts** | **43% churn rate** vs only 3% on 2-year contracts | Offer contract upgrade discounts (15–25% off) |
| **Early tenure (< 12 mos)** | **68% of all churn** occurs in the first year | Early loyalty rewards & dedicated account management |
| **Fiber optic subscribers** | Churn **2× more** than DSL users due to pricing pressure | Offer free security & device protection bundles |
| **Electronic check payments** | Highest churn rate among all payment methods | Incentivize auto-pay (5% bill credit) |

---

## 🛠️ Tech Stack

| Layer | Technologies |
|---|---|
| **Backend & Server** | Python 3, Flask, Gunicorn WSGI Server |
| **Machine Learning** | Scikit-learn (Random Forest, StandardScaler), Joblib, Pandas, NumPy |
| **Frontend UI** | HTML5, Vanilla CSS3 (Glassmorphism, High-Contrast Dark Mode), JavaScript (Fetch API) |
| **Typography & Icons** | Google Fonts (Inter), Modern Emoji Badges |
| **Deployment & Hosting** | Render.com (Web Service), Railway, Git |

---

## 📁 Project Structure

```
Customer-Churn-Prediction-Retention-Intelligence-System/
├── server.py                   # Flask server (API endpoints & model inference)
├── templates/
│   └── index.html              # Modern dark-themed frontend UI
├── static/
│   └── style.css               # Glassmorphism styling, responsive layouts & variables
├── columns.json                # Preprocessed feature column schema
├── rf_model.pkl                # Trained Random Forest model (production)
├── scaler.pkl                  # Fitted StandardScaler object
├── lr_model.pkl                # Trained Logistic Regression baseline
├── Customer_Churn_Project.ipynb# Full EDA, preprocessing, training & validation notebook
├── Customer-Churn.csv          # Local raw dataset
├── requirements.txt            # Python dependencies (Flask, Gunicorn, ML libs)
├── Procfile                    # Web process command for Render/Railway
├── app.py                      # Original Streamlit app (kept for legacy reference)
└── README.md                   # Documentation
```

---

## 🚀 How to Run Locally

### 1. Clone the Repository
```bash
git clone https://github.com/saicharan-r02/Customer-Churn-System.git
cd Customer-Churn-System
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Start the Flask Server
```bash
python server.py
```

### 4. Open in Browser
Visit **`http://localhost:5000`** in your browser.

---

## 🌐 Step-by-Step Cloud Deployment on Render.com

[Render](https://render.com) provides free and reliable cloud hosting for Python web applications. Follow these steps:

### Step 1: Push Code to GitHub
Ensure all your latest changes are pushed to your GitHub repository:
```bash
git add .
git commit -m "chore: prepare for Render deployment"
git push origin main
```

### Step 2: Create a Render Account
1. Go to [https://render.com](https://render.com) and click **Sign Up** (Sign in with your GitHub account for easiest setup).

### Step 3: Create a New Web Service
1. In your Render Dashboard, click **New +** → select **Web Service**.
2. Choose **Build and deploy from a Git repository**.
3. Connect your repository: `Customer-Churn-System` (or search for your repository name).

### Step 4: Configure Service Settings
Fill in the following configuration fields:

| Field | Value |
|---|---|
| **Name** | `customer-churn-intelligence` *(or any unique name)* |
| **Region** | Select the closest region (e.g., *Singapore*, *Frankfurt*, *Oregon*) |
| **Branch** | `main` |
| **Root Directory** | *(Leave empty)* |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn server:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120` |
| **Instance Type** | **Free** |

### Step 5: Deploy
1. Click **Create Web Service** at the bottom of the page.
2. Render will automatically clone your repository, install dependencies from `requirements.txt`, load the model, and start the Gunicorn server.
3. Once the build finishes and status shows **Live**, your public URL will appear at the top (e.g., `https://customer-churn-intelligence.onrender.com`).

---

## 📡 REST API Documentation

You can integrate predictions directly into other applications using the `/predict` endpoint:

### Endpoint: `POST /predict`
- **Content-Type**: `application/json`

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

#### Response Example (HTTP 200):
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

Built as an end-to-end production Machine Learning & Business Intelligence system.
