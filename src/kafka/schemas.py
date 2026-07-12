from datetime import datetime, timezone
from typing import Any, Dict, Literal, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class BaseEvent(BaseModel):
    event_id: UUID = Field(default_factory=uuid4)
    event_type: str
    occurred_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class CustomerPayload(BaseModel):
    customer_id: Optional[int] = None
    Age: int
    Gender: str
    Tenure: int
    Usage_Frequency: int = Field(alias="Usage Frequency")
    Support_Calls: int = Field(alias="Support Calls")
    Payment_Delay: int = Field(alias="Payment Delay")
    Subscription_Type: str = Field(alias="Subscription Type")
    Contract_Length: str = Field(alias="Contract Length")
    Total_Spend: float = Field(alias="Total Spend")
    Last_Interaction: int = Field(alias="Last Interaction")

    model_config = {
        "populate_by_name": True
    }


class CustomerCreatedEvent(BaseEvent):
    event_type: Literal["CustomerCreated"] = "CustomerCreated"
    payload: CustomerPayload


class CustomerUpdatedEvent(BaseEvent):
    event_type: Literal["CustomerUpdated"] = "CustomerUpdated"
    payload: CustomerPayload


class PredictionPayload(BaseModel):
    customer_id: int

    customer_data: CustomerPayload

    predicted_churn: bool
    churn_probability: float
    risk_level: Literal["LOW", "MEDIUM", "HIGH"]
    model_version: str


class PredictionCreatedEvent(BaseEvent):
    event_type: Literal["PredictionCreated"] = "PredictionCreated"
    payload: PredictionPayload


class RiskEscalatedPayload(BaseModel):
    customer_id: int
    previous_risk_level: str
    current_risk_level: str
    risk_transition: str


class RiskEscalatedEvent(BaseEvent):
    event_type: Literal["RiskEscalated"] = "RiskEscalated"
    payload: RiskEscalatedPayload