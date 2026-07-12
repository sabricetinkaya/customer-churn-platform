from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CustomerResponse(BaseModel):
    customer_id: int

    age: Optional[int] = None
    gender: Optional[str] = None
    tenure: Optional[int] = None
    usage_frequency: Optional[int] = None
    support_calls: Optional[int] = None
    payment_delay: Optional[int] = None
    subscription_type: Optional[str] = None
    contract_length: Optional[str] = None
    total_spend: Optional[float] = None
    last_interaction: Optional[int] = None

    current_prediction: Optional[bool] = None
    current_churn_probability: Optional[float] = None
    current_risk_level: Optional[str] = None

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }


class PredictionHistoryResponse(BaseModel):
    prediction_id: int
    customer_id: int

    churn_probability: float
    predicted_churn: bool
    risk_level: str

    previous_risk_level: Optional[str] = None
    risk_transition: str

    model_version: str
    created_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }