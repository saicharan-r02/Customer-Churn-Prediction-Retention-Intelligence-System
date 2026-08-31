"""
Flask server for Customer Churn Prediction & Retention Intelligence System
Replaces the Streamlit app with a real deployable web server.
"""

import sys
import os

# Ensure UTF-8 output on Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

import json
import joblib
import numpy as np
import pandas as pd
from flask import Flask, render_template, request, jsonify

app=Flask(__name__)

#Load models once at startup 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model=joblib.load(os.path.join(BASE_DIR,"rf_model.pkl"))
scaler=joblib.load(os.path.join(BASE_DIR,"scaler.pkl"))

with open(os.path.join(BASE_DIR,"columns.json")) as f:
    COLUMNS=json.load(f)

print("[OK] Models loaded successfully.")


#Retention intelligence logic (ported from app.py) 
def get_retention_intelligence(data: dict) -> tuple:
    contract=data["contract"]
    internet=data["internet"]
    payment=data["payment"]
    tenure=data["tenure"]
    monthly_charges=data["monthly_charges"]
    senior=data["senior"]
    tech_support=data["tech_support"]
    online_security=data["online_security"]
    online_backup=data["online_backup"]
    streaming_tv=data["streaming_tv"]
    streaming_movies=data["streaming_movies"]

    risk_factors=[]
    actions=[]

    if contract=="Month-to-month":
        risk_factors.append(
            "Month-to-month contract — these customers have a 43% churn rate "
            "vs only 3% for 2-year contracts"
        )
        actions.append({
            "title":"🔒 Offer contract upgrade",
            "desc":"Propose a 1-year contract with 15% monthly discount "
                     "or a 2-year contract with 25% discount"
        })

    if internet=="Fiber optic":
        risk_factors.append(
            "Fiber optic subscriber — churns 2× more than DSL users "
            "(likely due to higher cost and more competition)"
        )
        if online_security=="No":
            actions.append({
                "title":"🛡️ Free security bundle",
                "desc":"Add Online Security + Device Protection free for 3 months "
                         "— increases service stickiness"
            })
        if tech_support=="No":
            actions.append({
                "title":"🛠️ Tech support upgrade",
                "desc":"Offer Tech Support package at 50% off for the first year "
                         "to reduce service frustration"
            })

    if payment=="Electronic check":
        risk_factors.append(
            "Electronic check payment — highest churn rate among all payment methods, "
            "linked to manual payment friction"
        )
        actions.append({
            "title":"💳 Auto-pay discount",
            "desc":"Offer a 5% monthly bill discount for switching to "
                     "bank transfer or credit card auto-pay"
        })

    if tenure<12:
        risk_factors.append(
            f"Low tenure ({tenure} months) — 68% of all churners leave within "
            "the first 12 months before building loyalty"
        )
        actions.append({
            "title":"🎁 Early loyalty programme",
            "desc":"Assign a dedicated account manager for first year + "
                     f"offer a loyalty gift at 12-month mark (e.g. 1 month free)"
        })

    if monthly_charges>80:
        saving=round(monthly_charges*0.10,2)
        risk_factors.append(
            f"High monthly charges (${monthly_charges:.0f}) — "
            "above-average bill increases price sensitivity and competitor appeal"
        )
        actions.append({
            "title":"💰 Loyalty price reduction",
            "desc":f"Offer a 10% loyalty discount (saves ${saving:.0f}/month) "
                     "for a 6-month service commitment"
        })

    if senior=="Yes" and tech_support=="No":
        risk_factors.append(
            "Senior citizen without tech support — "
            "higher likelihood of service frustration and passive churn"
        )
        actions.append({
            "title":"📞 Senior care plan",
            "desc":"Provide complimentary tech support + dedicated priority "
                     "customer service line for senior accounts"
        })

    has_internet=(internet!="No")
    no_streaming=(streaming_tv=="No" and streaming_movies=="No" and has_internet)
    no_security=(online_security=="No" and online_backup=="No" and has_internet)

    if no_streaming and no_security:
        actions.append({
            "title":"📺 Value bundle trial",
            "desc":"3-month free trial of Streaming TV + Movies + Online Security — "
                     "more services = much lower churn probability"
        })
    elif no_streaming:
        actions.append({
            "title":"📺 Streaming trial",
            "desc":"Free 3-month Streaming TV + Movies trial — "
                     "customers with streaming services churn significantly less"
        })

    if not risk_factors:
        risk_factors.append("No major risk factors detected for this customer")
        actions.append({
            "title":"⭐ Upsell opportunity",
            "desc":"Customer is satisfied — consider upselling premium services "
                     "or offering a loyalty reward at next contract renewal"
        })

    return risk_factors[:3],actions[:3]


#routes
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/predict",methods=["POST"])
def predict():
    try:
        data=request.get_json(force=True)

        #Map 3-value categorical columns
        le_3val={
            "MultipleLines":{"No":0,"No phone service":1,"Yes":2},
            "OnlineSecurity":{"No":0,"No internet service":1,"Yes":2},
            "OnlineBackup":{"No":0,"No internet service":1,"Yes":2},
            "DeviceProtection":{"No":0,"No internet service":1,"Yes":2},
            "TechSupport":{"No":0,"No internet service":1,"Yes":2},
            "StreamingTV":{"No":0,"No internet service":1,"Yes":2},
            "StreamingMovies":{"No":0,"No internet service":1,"Yes":2},
        }

        tenure=int(data.get("tenure",12))
        monthly_charges =float(data.get("monthly_charges",65.0))
        total_charges =float(data.get("total_charges",monthly_charges*max(tenure,1)))
        gender =data.get("gender","Female")
        senior =data.get("senior","No")
        partner =data.get("partner","No")
        dependents=data.get("dependents","No")
        phone=data.get("phone","Yes")
        multiple_lines=data.get("multiple_lines","No")
        internet=data.get("internet","DSL")
        online_security=data.get("online_security","No")
        online_backup=data.get("online_backup","No")
        device_prot=data.get("device_protection","No")
        tech_support=data.get("tech_support","No")
        streaming_tv=data.get("streaming_tv","No")
        streaming_movies=data.get("streaming_movies","No")
        paperless=data.get("paperless","No")
        contract=data.get("contract","Month-to-month")
        payment=data.get("payment","Electronic check")

        input_dict={
            "gender":0 if gender=="Female" else 1,
            "SeniorCitizen":1 if senior=="Yes" else 0,
            "Partner":0 if partner=="No" else 1,
            "Dependents":0 if dependents=="No" else 1,
            "tenure":tenure,
            "PhoneService":0 if phone=="No" else 1,
            "MultipleLines":le_3val["MultipleLines"][multiple_lines],
            "OnlineSecurity":le_3val["OnlineSecurity"][online_security],
            "OnlineBackup":le_3val["OnlineBackup"][online_backup],
            "DeviceProtection":le_3val["DeviceProtection"][device_prot],
            "TechSupport":le_3val["TechSupport"][tech_support],
            "StreamingTV":le_3val["StreamingTV"][streaming_tv],
            "StreamingMovies":le_3val["StreamingMovies"][streaming_movies],
            "PaperlessBilling":0 if paperless=="No" else 1,
            "MonthlyCharges":monthly_charges,
            "TotalCharges":total_charges,
            "InternetService_Fiber optic":1 if internet=="Fiber optic" else 0,
            "InternetService_No":1 if internet=="No" else 0,
            "Contract_One year":1 if contract=="One year" else 0,
            "Contract_Two year":1 if contract=="Two year" else 0,
            "PaymentMethod_Credit card (automatic)":1 if payment=="Credit card (automatic)" else 0,
            "PaymentMethod_Electronic check":1 if payment=="Electronic check" else 0,
            "PaymentMethod_Mailed check":1 if payment=="Mailed check" else 0,
        }

        input_df=pd.DataFrame([input_dict])[COLUMNS]
        scaled=scaler.transform(input_df)
        prob=float(model.predict_proba(scaled)[0][1])

        if prob<0.30:
            risk_level="LOW"
        elif prob<0.60:
            risk_level="MEDIUM"
        else:
            risk_level="HIGH"

        ri_data={
            "contract": contract,"internet": internet,"payment": payment,
            "tenure": tenure,"monthly_charges": monthly_charges,
            "senior": senior,"tech_support": tech_support,
            "online_security": online_security,"online_backup": online_backup,
            "streaming_tv": streaming_tv,"streaming_movies": streaming_movies,
        }
        risk_factors,actions=get_retention_intelligence(ri_data)

        return jsonify({
            "probability":round(prob*100,1),
            "risk_level":risk_level,
            "risk_factors":risk_factors,
            "actions":actions,
        })

    except Exception as e:
        return jsonify({"error":str(e)}),500


if __name__=="__main__":
    port=int(os.environ.get("PORT",5000))
    debug=os.environ.get("FLASK_ENV","production")=="development"
    print(f"[START] Server running at http://localhost:{port}")
    app.run(host="0.0.0.0",port=port,debug=debug)