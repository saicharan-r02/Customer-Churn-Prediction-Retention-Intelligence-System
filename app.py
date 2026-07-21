import streamlit as st
import pandas as pd
import numpy as np
import joblib
import json

@st.cache_resource
def load_model():
    model=joblib.load('rf_model.pkl')
    scaler=joblib.load('scaler.pkl')
    with open('columns.json') as f:
        columns=json.load(f)
    return model,scaler,columns

model,scaler,columns=load_model()

st.set_page_config(
    page_title="Churn Prediction & Retention Intelligence",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Customer Churn Prediction & Retention Intelligence System")
st.write("Predict which customers are at risk of leaving — and get a personalised plan to retain them.")
st.divider()

col1,col2,col3=st.columns(3)

with col1:
    st.subheader("📋 Account")
    tenure    =st.slider("Tenure (months)", 0, 72, 12)
    contract  =st.selectbox("Contract",
                    ["Month-to-month", "One year", "Two year"])
    payment   =st.selectbox("Payment Method", [
                    "Bank transfer (automatic)",
                    "Credit card (automatic)",
                    "Electronic check",
                    "Mailed check"])
    paperless =st.selectbox("Paperless Billing", ["No", "Yes"])

with col2:
    st.subheader("🌐 Services")
    phone            =st.selectbox("Phone Service", ["No", "Yes"])
    multiple_lines   =st.selectbox("Multiple Lines",
                            ["No", "No phone service", "Yes"])
    internet         =st.selectbox("Internet Service",
                            ["DSL", "Fiber optic", "No"])
    online_security  =st.selectbox("Online Security",
                            ["No", "No internet service", "Yes"])
    online_backup    =st.selectbox("Online Backup",
                            ["No", "No internet service", "Yes"])
    device_prot      =st.selectbox("Device Protection",
                            ["No", "No internet service", "Yes"])
    tech_support     =st.selectbox("Tech Support",
                            ["No", "No internet service", "Yes"])
    streaming_tv     =st.selectbox("Streaming TV",
                            ["No", "No internet service", "Yes"])
    streaming_movies =st.selectbox("Streaming Movies",
                            ["No", "No internet service", "Yes"])

with col3:
    st.subheader("👤 Demographics & Charges")
    gender          =st.selectbox("Gender", ["Female", "Male"])
    senior          =st.selectbox("Senior Citizen", ["No", "Yes"])
    partner         =st.selectbox("Partner", ["No", "Yes"])
    dependents      =st.selectbox("Dependents", ["No", "Yes"])
    monthly_charges =st.slider("Monthly Charges ($)", 18.0, 120.0, 65.0)
    total_charges   =st.number_input(
                        "Total Charges ($)",min_value=0.0,max_value=9000.0,
                        value=float(round(monthly_charges*max(tenure,1),2)))

st.divider()

def get_retention_intelligence():
    """
    Analyse this customer's profile and return:
      - risk_factors :list of strings explaining WHY they might churn
      - actions      :list of (title, description) specific retention steps
    Based on EDA insights from the training dataset.
    """
    risk_factors =[]
    actions      =[]


    if contract=="Month-to-month":
        risk_factors.append(
            "Month-to-month contract — these customers have a 43% churn rate "
            "vs only 3% for 2-year contracts")
        actions.append((
            "🔒 Offer contract upgrade",
            "Propose a 1-year contract with 15% monthly discount "
            "or a 2-year contract with 25% discount"))


    if internet=="Fiber optic":
        risk_factors.append(
            "Fiber optic subscriber — churns 2× more than DSL users "
            "(likely due to higher cost and more competition)")
        if online_security == "No":
            actions.append((
                "🛡️ Free security bundle",
                "Add Online Security + Device Protection free for 3 months "
                "— increases service stickiness"))
        if tech_support=="No":
            actions.append((
                "🛠️ Tech support upgrade",
                "Offer Tech Support package at 50% off for the first year "
                "to reduce service frustration"))

    if payment=="Electronic check":
        risk_factors.append(
            "Electronic check payment — highest churn rate among all payment methods, "
            "linked to manual payment friction")
        actions.append((
            "💳 Auto-pay discount",
            "Offer a 5% monthly bill discount for switching to "
            "bank transfer or credit card auto-pay"))


    if tenure<12:
        risk_factors.append(
            f"Low tenure ({tenure} months) — 68% of all churners leave within "
            "the first 12 months before building loyalty")
        actions.append((
            "🎁 Early loyalty programme",
            "Assign a dedicated account manager for first year + "
            f"offer a loyalty gift at 12-month mark (e.g. 1 month free)"))

    if monthly_charges>80:
        saving=round(monthly_charges*0.10, 2)
        risk_factors.append(
            f"High monthly charges (${monthly_charges:.0f}) — "
            "above-average bill increases price sensitivity and competitor appeal")
        actions.append((
            "💰 Loyalty price reduction",
            f"Offer a 10% loyalty discount (saves ${saving:.0f}/month) "
            "for a 6-month service commitment"))


    if senior=="Yes" and tech_support=="No":
        risk_factors.append(
            "Senior citizen without tech support — "
            "higher likelihood of service frustration and passive churn")
        actions.append((
            "📞 Senior care plan",
            "Provide complimentary tech support + dedicated priority "
            "customer service line for senior accounts"))


    has_internet=(internet!="No")
    no_streaming=(streaming_tv=="No" and streaming_movies=="No" and has_internet)
    no_security=(online_security=="No" and online_backup=="No" and has_internet)

    if no_streaming and no_security:
        actions.append((
            "📺 Value bundle trial",
            "3-month free trial of Streaming TV + Movies + Online Security — "
            "more services = much lower churn probability"))
    elif no_streaming:
        actions.append((
            "📺 Streaming trial",
            "Free 3-month Streaming TV + Movies trial — "
            "customers with streaming services churn significantly less"))

    if not risk_factors:
        risk_factors.append("No major risk factors detected for this customer")
        actions.append((
            "⭐ Upsell opportunity",
            "Customer is satisfied — consider upselling premium services "
            "or offering a loyalty reward at next contract renewal"))

    return risk_factors[:3],actions[:3]

if st.button("🔍 Predict & Get Retention Plan",
             use_container_width=True, type="primary"):

    le_3val = {
        'MultipleLines':    {'No': 0, 'No phone service': 1, 'Yes': 2},
        'OnlineSecurity':   {'No': 0, 'No internet service': 1, 'Yes': 2},
        'OnlineBackup':     {'No': 0, 'No internet service': 1, 'Yes': 2},
        'DeviceProtection': {'No': 0, 'No internet service': 1, 'Yes': 2},
        'TechSupport':      {'No': 0, 'No internet service': 1, 'Yes': 2},
        'StreamingTV':      {'No': 0, 'No internet service': 1, 'Yes': 2},
        'StreamingMovies':  {'No': 0, 'No internet service': 1, 'Yes': 2},
    }

    input_dict = {
        'gender':           0 if gender=="Female" else 1,
        'SeniorCitizen':    1 if senior=="Yes" else 0,
        'Partner':          0 if partner=="No" else 1,
        'Dependents':       0 if dependents=="No" else 1,
        'tenure':           tenure,
        'PhoneService':     0 if phone=="No" else 1,
        'MultipleLines':    le_3val['MultipleLines'][multiple_lines],
        'OnlineSecurity':   le_3val['OnlineSecurity'][online_security],
        'OnlineBackup':     le_3val['OnlineBackup'][online_backup],
        'DeviceProtection': le_3val['DeviceProtection'][device_prot],
        'TechSupport':      le_3val['TechSupport'][tech_support],
        'StreamingTV':      le_3val['StreamingTV'][streaming_tv],
        'StreamingMovies':  le_3val['StreamingMovies'][streaming_movies],
        'PaperlessBilling': 0 if paperless=="No" else 1,
        'MonthlyCharges':   monthly_charges,
        'TotalCharges':     total_charges,
        'InternetService_Fiber optic': 1 if internet=="Fiber optic" else 0,
        'InternetService_No':          1 if internet=="No" else 0,
        'Contract_One year':           1 if contract=="One year" else 0,
        'Contract_Two year':           1 if contract=="Two year" else 0,
        'PaymentMethod_Credit card (automatic)':
            1 if payment=="Credit card (automatic)" else 0,
        'PaymentMethod_Electronic check':
            1 if payment=="Electronic check" else 0,
        'PaymentMethod_Mailed check':
            1 if payment=="Mailed check" else 0,
    }

    input_df=pd.DataFrame([input_dict])
    input_df=input_df[columns]

    scaled=scaler.transform(input_df)
    pred =model.predict(scaled)[0]
    prob =model.predict_proba(scaled)[0][1]


    if prob<0.30:
        risk_level,risk_icon="LOW", "✅"
    elif prob < 0.60:
        risk_level, risk_icon="MEDIUM", "⚠️"
    else:
        risk_level, risk_icon="HIGH", "🚨"

    left,right=st.columns([1, 2])

    with left:
        st.markdown("### Churn Risk Score")
        if risk_level=="LOW":
            st.success(f"{risk_icon} **{risk_level} RISK**\n\n"
                       f"Churn probability: **{prob*100:.1f}%**")
        elif risk_level=="MEDIUM":
            st.warning(f"{risk_icon} **{risk_level} RISK**\n\n"
                       f"Churn probability: **{prob*100:.1f}%**")
        else:
            st.error(f"{risk_icon} **{risk_level} RISK**\n\n"
                     f"Churn probability: **{prob*100:.1f}%**")

        st.progress(prob,text=f"{prob*100:.1f}% likelihood to leave")

        st.markdown("**Risk thresholds:**")
        st.markdown("- 🟢 0–30% → Low risk")
        st.markdown("- 🟡 30–60% → Medium risk")
        st.markdown("- 🔴 60–100% → High risk")

    with right:
        risk_factors,actions=get_retention_intelligence()

        st.markdown("### 🎯 Why This Customer Is at Risk")
        if risk_factors and risk_factors[0] != "No major risk factors detected for this customer":
            for rf in risk_factors:
                st.warning(f"• {rf}")
        else:
            st.success("• No major risk factors — customer profile is stable")

        st.markdown("### 💡 Personalised Retention Actions")
        for i, (title, desc) in enumerate(actions, 1):
            with st.container():
                st.markdown(f"**Action {i}: {title}**")
                st.info(desc)
