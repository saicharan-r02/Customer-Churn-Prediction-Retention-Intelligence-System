"""
Database module for Customer Churn Prediction & Retention Intelligence System.
Uses SQLite and SQLAlchemy for enterprise CRM audit logging, prediction history, and retention outcome tracking.
"""

import os
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple

from sqlalchemy import (
    create_engine, Column, Integer, Float, String, Boolean, DateTime, JSON, ForeignKey, func
)
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, scoped_session

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "churn_intelligence.db")
DATABASE_URI = f"sqlite:///{DB_PATH}"

engine = create_engine(DATABASE_URI, connect_args={"check_same_thread": False})
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()


class Customer(Base):
    """Stores customer profile and contract specifications."""
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_code = Column(String(50), index=True, nullable=True)
    gender = Column(String(10), default="Unknown")
    senior_citizen = Column(Boolean, default=False)
    partner = Column(Boolean, default=False)
    dependents = Column(Boolean, default=False)
    tenure = Column(Integer, default=0)
    contract = Column(String(50), default="Month-to-month")
    payment_method = Column(String(50), default="Electronic check")
    monthly_charges = Column(Float, default=0.0)
    total_charges = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    predictions = relationship("ChurnPrediction", back_populates="customer", cascade="all, delete-orphan")


class ChurnPrediction(Base):
    """Stores every ML inference result with full audit trail."""
    __tablename__ = "churn_predictions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    churn_probability = Column(Float, nullable=False)
    risk_level = Column(String(20), nullable=False)  # LOW, MEDIUM, HIGH
    risk_factors = Column(JSON, default=list)
    recommended_actions = Column(JSON, default=list)
    predicted_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    customer = relationship("Customer", back_populates="predictions")
    retention_outcome = relationship("RetentionOutcome", back_populates="prediction", uselist=False, cascade="all, delete-orphan")


class RetentionOutcome(Base):
    """Tracks whether prescribed retention actions were accepted or declined."""
    __tablename__ = "retention_outcomes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    prediction_id = Column(Integer, ForeignKey("churn_predictions.id"), nullable=False, unique=True)
    action_taken = Column(String(200), nullable=True)
    status = Column(String(50), default="PENDING")  # PENDING, ACCEPTED, DECLINED, CHURNED
    notes = Column(String(500), nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    prediction = relationship("ChurnPrediction", back_populates="retention_outcome")


def init_db():
    """Initializes tables in the SQLite database."""
    Base.metadata.create_all(bind=engine)
    print(f"[OK] Database initialized at: {DB_PATH}")


def log_prediction(
    customer_data: Dict[str, Any],
    churn_prob: float,
    risk_level: str,
    risk_factors: List[str],
    recommended_actions: List[Dict[str, str]]
) -> int:
    """Logs customer data, prediction results, and generates a retention outcome record."""
    session = SessionLocal()
    try:
        # Create Customer record
        customer = Customer(
            customer_code=customer_data.get("customer_id") or f"CUST-{int(datetime.utcnow().timestamp())}",
            gender=customer_data.get("gender", "Female"),
            senior_citizen=(customer_data.get("senior") == "Yes"),
            partner=(customer_data.get("partner") == "Yes"),
            dependents=(customer_data.get("dependents") == "Yes"),
            tenure=int(customer_data.get("tenure", 1)),
            contract=customer_data.get("contract", "Month-to-month"),
            payment_method=customer_data.get("payment", "Electronic check"),
            monthly_charges=float(customer_data.get("monthly_charges", 0.0)),
            total_charges=float(customer_data.get("total_charges", 0.0))
        )
        session.add(customer)
        session.flush()

        # Create ChurnPrediction record
        prediction = ChurnPrediction(
            customer_id=customer.id,
            churn_probability=float(churn_prob),
            risk_level=risk_level,
            risk_factors=risk_factors,
            recommended_actions=recommended_actions
        )
        session.add(prediction)
        session.flush()

        # Create initial RetentionOutcome record
        primary_action = recommended_actions[0].get("title") if recommended_actions else "Monitor Account"
        outcome = RetentionOutcome(
            prediction_id=prediction.id,
            action_taken=primary_action,
            status="PENDING",
            notes="Awaiting retention outreach"
        )
        session.add(outcome)
        session.commit()
        return prediction.id
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def get_recent_predictions(limit: int = 20) -> List[Dict[str, Any]]:
    """Fetches recent predictions with joined customer and outcome information."""
    session = SessionLocal()
    try:
        records = (
            session.query(ChurnPrediction)
            .join(Customer)
            .outerjoin(RetentionOutcome)
            .order_by(ChurnPrediction.predicted_at.desc())
            .limit(limit)
            .all()
        )

        results = []
        for p in records:
            outcome = p.retention_outcome
            results.append({
                "prediction_id": p.id,
                "customer_code": p.customer.customer_code,
                "tenure": p.customer.tenure,
                "contract": p.customer.contract,
                "monthly_charges": p.customer.monthly_charges,
                "churn_probability": round(p.churn_probability, 1),
                "risk_level": p.risk_level,
                "risk_factors": p.risk_factors,
                "recommended_actions": p.recommended_actions,
                "predicted_at": p.predicted_at.strftime("%Y-%m-%d %H:%M:%S") if p.predicted_at else None,
                "retention_status": outcome.status if outcome else "PENDING",
                "action_taken": outcome.action_taken if outcome else None,
            })
        return results
    finally:
        session.close()


def get_analytics_summary() -> Dict[str, Any]:
    """Computes high-level CRM churn metrics across the database."""
    session = SessionLocal()
    try:
        total = session.query(func.count(ChurnPrediction.id)).scalar() or 0
        if total == 0:
            return {
                "total_predictions": 0,
                "avg_churn_rate": 0.0,
                "risk_distribution": {"LOW": 0, "MEDIUM": 0, "HIGH": 0},
                "retention_stats": {"PENDING": 0, "ACCEPTED": 0, "DECLINED": 0, "CHURNED": 0}
            }

        avg_prob = session.query(func.avg(ChurnPrediction.churn_probability)).scalar() or 0.0
        
        low_count = session.query(func.count(ChurnPrediction.id)).filter(ChurnPrediction.risk_level == "LOW").scalar() or 0
        med_count = session.query(func.count(ChurnPrediction.id)).filter(ChurnPrediction.risk_level == "MEDIUM").scalar() or 0
        high_count = session.query(func.count(ChurnPrediction.id)).filter(ChurnPrediction.risk_level == "HIGH").scalar() or 0

        pending_count = session.query(func.count(RetentionOutcome.id)).filter(RetentionOutcome.status == "PENDING").scalar() or 0
        accepted_count = session.query(func.count(RetentionOutcome.id)).filter(RetentionOutcome.status == "ACCEPTED").scalar() or 0
        declined_count = session.query(func.count(RetentionOutcome.id)).filter(RetentionOutcome.status == "DECLINED").scalar() or 0
        churned_count = session.query(func.count(RetentionOutcome.id)).filter(RetentionOutcome.status == "CHURNED").scalar() or 0

        return {
            "total_predictions": total,
            "avg_churn_rate": round(float(avg_prob), 1),
            "risk_distribution": {
                "LOW": low_count,
                "MEDIUM": med_count,
                "HIGH": high_count
            },
            "retention_stats": {
                "PENDING": pending_count,
                "ACCEPTED": accepted_count,
                "DECLINED": declined_count,
                "CHURNED": churned_count
            }
        }
    finally:
        session.close()


def update_retention_status(prediction_id: int, status: str, action_taken: Optional[str] = None, notes: Optional[str] = None) -> bool:
    """Updates retention campaign progress for a specific prediction."""
    session = SessionLocal()
    try:
        outcome = session.query(RetentionOutcome).filter(RetentionOutcome.prediction_id == prediction_id).first()
        if not outcome:
            return False
        
        outcome.status = status
        if action_taken:
            outcome.action_taken = action_taken
        if notes:
            outcome.notes = notes
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


if __name__ == "__main__":
    init_db()
