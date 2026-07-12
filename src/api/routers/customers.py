from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.api.dependencies import get_db
from src.api.schemas import CustomerPayload, EventAcceptedResponse
from src.database.repository import (
    get_customer_by_id,
    get_prediction_history_by_customer_id,
)
from src.database.schemas import CustomerResponse, PredictionHistoryResponse
from src.kafka.config import get_kafka_settings
from src.kafka.producer import get_event_producer
from src.kafka.schemas import (
    CustomerPayload as KafkaCustomerPayload,
    CustomerCreatedEvent,
    CustomerUpdatedEvent,
)


router = APIRouter(prefix="/customers", tags=["customers"])


@router.post("", response_model=EventAcceptedResponse)
def create_customer(customer: CustomerPayload):
    settings = get_kafka_settings()
    producer = get_event_producer()

    payload = customer.model_dump(by_alias=True)
    payload["customer_id"] = customer.customer_id

    event = CustomerCreatedEvent(
        payload=KafkaCustomerPayload(**payload)
    )

    producer.publish(
        topic=settings.customer_topic,
        event=event,
    )

    return EventAcceptedResponse(
        status="ACCEPTED",
        message="CustomerCreated event published successfully.",
        customer_id=customer.customer_id,
    )


@router.put("/{customer_id}", response_model=EventAcceptedResponse)
def update_customer(customer_id: int, customer: CustomerPayload):
    settings = get_kafka_settings()
    producer = get_event_producer()

    payload = customer.model_dump(by_alias=True)
    payload["customer_id"] = customer_id

    event = CustomerUpdatedEvent(
        payload=KafkaCustomerPayload(**payload)
    )

    producer.publish(
        topic=settings.customer_topic,
        event=event,
    )

    return EventAcceptedResponse(
        status="ACCEPTED",
        message="CustomerUpdated event published successfully.",
        customer_id=customer_id,
    )


@router.get("/{customer_id}", response_model=CustomerResponse)
def read_customer(
    customer_id: int,
    db: Session = Depends(get_db),
):
    customer = get_customer_by_id(db, customer_id)

    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    return customer


@router.get("/{customer_id}/history", response_model=list[PredictionHistoryResponse])
def read_customer_history(
    customer_id: int,
    db: Session = Depends(get_db),
):
    return get_prediction_history_by_customer_id(db, customer_id)