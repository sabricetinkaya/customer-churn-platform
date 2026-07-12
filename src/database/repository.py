# src/database/repository.py

from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database.models import Customer, PredictionHistory
from src.inference.risk import get_risk_transition


def get_customer_by_id(
    db: Session,
    customer_id: int,
) -> Optional[Customer]:
    stmt = select(Customer).where(Customer.customer_id == customer_id)
    return db.execute(stmt).scalar_one_or_none()


def get_prediction_history_by_customer_id(
    db: Session,
    customer_id: int,
) -> list[PredictionHistory]:
    stmt = (
        select(PredictionHistory)
        .where(PredictionHistory.customer_id == customer_id)
        .order_by(PredictionHistory.created_at.desc())
    )

    return list(db.execute(stmt).scalars().all())


def get_risk_increased_customers(
    db: Session,
) -> list[PredictionHistory]:
    increased_transitions = [
        "LOW_TO_MEDIUM",
        "LOW_TO_HIGH",
        "MEDIUM_TO_HIGH",
    ]

    stmt = (
        select(PredictionHistory)
        .where(PredictionHistory.risk_transition.in_(increased_transitions))
        .order_by(PredictionHistory.created_at.desc())
    )

    return list(db.execute(stmt).scalars().all())


def upsert_customer_prediction(
    db: Session,
    customer_id: int,
    prediction_payload: dict,
    customer_payload: Optional[dict] = None,
) -> PredictionHistory:
    customer = get_customer_by_id(db, customer_id)

    new_prediction = prediction_payload["predicted_churn"]
    new_probability = prediction_payload["churn_probability"]
    new_risk_level = prediction_payload["risk_level"]
    model_version = prediction_payload["model_version"]

    now = datetime.now(timezone.utc)

    if customer is None:
        customer = Customer(
            customer_id=customer_id,
            current_prediction=new_prediction,
            current_churn_probability=new_probability,
            current_risk_level=new_risk_level,
            created_at=now,
            updated_at=now,
        )

        if customer_payload:
            _apply_customer_payload(customer, customer_payload)

        db.add(customer)

        previous_risk_level = None

    else:
        previous_risk_level = customer.current_risk_level

        customer.current_prediction = new_prediction
        customer.current_churn_probability = new_probability
        customer.current_risk_level = new_risk_level
        customer.updated_at = now

        if customer_payload:
            _apply_customer_payload(customer, customer_payload)

    risk_transition = get_risk_transition(
        previous_risk=previous_risk_level,
        current_risk=new_risk_level,
    )

    history = PredictionHistory(
        customer_id=customer_id,
        churn_probability=new_probability,
        predicted_churn=new_prediction,
        risk_level=new_risk_level,
        previous_risk_level=previous_risk_level,
        risk_transition=risk_transition,
        model_version=model_version,
        created_at=now,
    )

    db.add(history)
    db.commit()
    db.refresh(history)

    return history


def _apply_customer_payload(
    customer: Customer,
    payload: dict,
) -> None:
    mapping = {
        "Age": "age",
        "Gender": "gender",
        "Tenure": "tenure",
        "Usage Frequency": "usage_frequency",
        "Support Calls": "support_calls",
        "Payment Delay": "payment_delay",
        "Subscription Type": "subscription_type",
        "Contract Length": "contract_length",
        "Total Spend": "total_spend",
        "Last Interaction": "last_interaction",
    }

    for source_key, model_attr in mapping.items():
        if source_key in payload:
            setattr(customer, model_attr, payload[source_key])