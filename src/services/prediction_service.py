# src/services/prediction_service.py

import logging

from src.inference.predictor import predict_customer

from src.kafka.config import get_kafka_settings
from src.kafka.consumer import EventConsumer
from src.kafka.event_types import (
    CUSTOMER_CREATED,
    CUSTOMER_UPDATED,
    PREDICTION_CREATED,
)
from src.kafka.producer import get_event_producer
from src.kafka.schemas import PredictionCreatedEvent, PredictionPayload


logger = logging.getLogger(__name__)


SUPPORTED_CUSTOMER_EVENTS = {
    CUSTOMER_CREATED,
    CUSTOMER_UPDATED,
}


def handle_customer_event(event: dict) -> None:
    event_type = event.get("event_type")

    if event_type not in SUPPORTED_CUSTOMER_EVENTS:
        logger.warning("Unsupported event_type=%s", event_type)
        return

    payload = event.get("payload")

    if not payload:
        logger.warning("Customer event has no payload. event_id=%s", event.get("event_id"))
        return

    logger.info(
        "Processing customer event_type=%s event_id=%s",
        event_type,
        event.get("event_id"),
    )

    try:
        prediction_result = predict_customer(payload)

        prediction_payload = PredictionPayload(
            customer_id=prediction_result["customer_id"],
            customer_data=payload,
            predicted_churn=prediction_result["predicted_churn"],
            churn_probability=prediction_result["churn_probability"],
            risk_level=prediction_result["risk_level"],
            model_version=prediction_result["model_version"],
        )

        prediction_event = PredictionCreatedEvent(
            event_type=PREDICTION_CREATED,
            payload=prediction_payload,
        )

        settings = get_kafka_settings()
        producer = get_event_producer()

        producer.publish(
            topic=settings.prediction_topic,
            event=prediction_event,
        )

        logger.info(
            "PredictionCreated published customer_id=%s probability=%.4f risk=%s",
            prediction_result["customer_id"],
            prediction_result["churn_probability"],
            prediction_result["risk_level"],
        )

    except Exception as exc:
        logger.exception("Prediction failed for event_id=%s error=%s", event.get("event_id"), exc)


def main() -> None:
    logging.basicConfig(level=logging.INFO)

    settings = get_kafka_settings()

    consumer = EventConsumer(
        topic=settings.customer_topic,
        group_id=settings.prediction_consumer_group,
    )

    logger.info("Prediction service started.")

    consumer.consume(handle_customer_event)


if __name__ == "__main__":
    main()