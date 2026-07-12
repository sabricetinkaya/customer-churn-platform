from pydantic import BaseModel, Field


class CustomerPayload(BaseModel):
    customer_id: int

    age: int = Field(alias="Age")
    gender: str = Field(alias="Gender")
    tenure: int = Field(alias="Tenure")
    usage_frequency: int = Field(alias="Usage Frequency")
    support_calls: int = Field(alias="Support Calls")
    payment_delay: int = Field(alias="Payment Delay")
    subscription_type: str = Field(alias="Subscription Type")
    contract_length: str = Field(alias="Contract Length")
    total_spend: float = Field(alias="Total Spend")
    last_interaction: int = Field(alias="Last Interaction")

    model_config = {
        "populate_by_name": True
    }


class EventAcceptedResponse(BaseModel):
    status: str
    message: str
    customer_id: int