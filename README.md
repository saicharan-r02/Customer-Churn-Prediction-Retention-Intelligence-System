# 📊 Customer Churn Prediction & Retention Intelligence System

> Predict which telecom customers are at risk of leaving — and get a personalised,data-driven plan to retain them.

🔴 **Live Demo**:[Click here to try the app](https://customer-cpris-7044.streamlit.app/)

---
## 🎯 Problem Statement

Customer churn is one of the most costly problems in the telecom industry. Acquiring a new customer costs **5–7× more** than retaining an existing one. Yet most companies only act after a customer has already left.

This project solves two problems in one system:
1. **Predict** —which customers are at risk of churning (and by how much)
2. **Retain** —give a personalised,specific action plan for each at-risk customer *before* they leave

---

## 💡 Solution

A machine learning system trained on **7,032 real Telco customer records** that:
- Classifies each customer into Low /Medium/High churn risk
- Explains *why* that specific customer is at risk
- Recommends personalised retention actions (contract offers, discounts, bundles, loyalty programmes)
- Deployed as a live interactive web application

---

## 🏆 Model Results

| Model | Accuracy | ROC-AUC |
|---|---|---|
| Logistic Regression | 79.3% | 0.830 |
| **Random Forest** ✅ | **80.4%** | **0.850** |
| Gradient Boosting | 80.1% | 0.845 |

**Winner: Random Forest** — best accuracy and AUC, selected for deployment.

---

## 📊 Key EDA Insights (from 7,032 customer records)

| Finding | Data |
|---|---|
| Month-to-month contract churn rate | **43%** vs 3% for 2-year contracts |
| Customers who churn in first 12 months | **68%** — critical early retention window |
| Fiber optic vs DSL churn rate | Fiber churns **2× more** than DSL |
| Highest-risk payment method | **Electronic check** — highest churn of all methods |

---

## 🧠 Retention Intelligence Logic

The system goes beyond a simple probability score. For each customer it analyses:

- **Contract type** → offers specific upgrade discount (15% for 1-yr, 25% for 2-yr)
- **Internet service** → recommends free security/tech bundle for fiber optic users
- **Payment method** → suggests auto-pay switch with 5% monthly discount
- **Tenure** → triggers early loyalty programme for customers under 12 months
- **Monthly charges** → calculates exact saving and proposes price reduction
- **Senior citizens** → recommends dedicated support plan
- **Missing services** → offers targeted streaming/security trial bundles

---

## 🛠️ Tech Stack

| Category | Tools |
|---|---|
| Language | Python 3 |
| Data Processing | Pandas, NumPy |
| Machine Learning | Scikit-learn (Random Forest, Logistic Regression, Gradient Boosting) |
| Visualisation | Matplotlib, Seaborn |
| Web App | Streamlit |
| Model Persistence | Joblib |
| Deployment | Streamlit Cloud |

---

## 📁 Project Structure

```
Customer-Churn-Prediction-Reten.../
├── .gitignore
├── app.py
├── columns.json
├── Customer_Churn_Project.ipynb
├── Customer-Churn.csv        ← stays local (gitignored)
├── lr_model.pkl
├── README.md                  
├── requirements.txt
├── rf_model.pkl
└── scaler.pkl
```

---

## 🚀 How to Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/saicharan-r02/Customer-Churn-Prediction-Retention-Intelligence-System.git
cd Customer-Churn-Prediction-Retention-Intelligence-System

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

---

## 📸 Screenshots

### Home — Input Form
<img width="1915" height="962" alt="Screenshot 2026-07-01 173534" src="https://github.com/user-attachments/assets/980c8e1f-50a1-4635-af10-38ad9996897d" />
<img width="1918" height="975" alt="Screenshot 2026-07-01 173607" src="https://github.com/user-attachments/assets/5d0f70b8-f0a8-4dc2-8759-cbeb6f1596fd" />


### Prediction — High Risk Customer
<img width="650" height="841" alt="Screenshot 2026-07-01 173624" src="https://github.com/user-attachments/assets/12275b78-d761-43e1-a5e7-f23ebf3063b6" />


### Prediction — Retention Actions
<img width="1258" height="890" alt="Screenshot 2026-07-01 173739" src="https://github.com/user-attachments/assets/53872666-2f4c-466f-b502-69a18128fcbc" />

---

## 📈 Dataset

- **Source**:IBM Telco Customer Churn Dataset (available on Kaggle)
- **Records**:7,043 customers → 7,032 after cleaning (11 rows with null TotalCharges dropped)
- **Features**:20 columns including demographics,services,contract, and charges
- **Target**:Churn (Yes/No)→encoded as 1/0

---

## 🔍 Notebook Sections

The training notebook (`Customer_Churn_Project.ipynb`) covers:

1. Data loading & initial exploration
2. Data cleaning (TotalCharges fix,null handling,encoding)
3. Exploratory Data Analysis — 12 plots across demographics and services
4. Feature preprocessing (LabelEncoder+get_dummies+StandardScaler)
5. Model building & comparison (LRvsRFvsGB)
6. ROC curve comparison + feature importance plot
7. Final results — confusion matrix+classification report

---
## 👨‍💻 Author
Built as an end-to-end machine learning project demonstrating data cleaning, EDA, model selection, and production deployment with a business-focused retention intelligence layer.
