# src/services/persistence_service.py

import logging

from src.database.database import SessionLocal
from src.database.repository import upsert_customer_prediction
from src.kafka.config import get_kafka_settings
from src.kafka.consumer import EventConsumer
from src.kafka.event_types import PREDICTION_CREATED


logger = logging.getLogger(__name__)


def save_prediction_event(event: dict) -> None:
    if event.get("event_type") != PREDICTION_CREATED:
        logger.warning("Unsupported event_type=%s", event.get("event_type"))
        return

    payload = event["payload"]

    customer_id = payload["customer_id"]
    customer_payload = payload.get("customer_data")

    db = SessionLocal()

    try:
        history = upsert_customer_prediction(
            db=db,
            customer_id=customer_id,
            prediction_payload=payload,
            customer_payload=customer_payload,
        )

        logger.info(
            "Prediction saved customer_id=%s prediction_id=%s risk=%s transition=%s",
            customer_id,
            history.prediction_id,
            history.risk_level,
            history.risk_transition,
        )

    except Exception as exc:
        db.rollback()
        logger.exception("Error while saving prediction event: %s", exc)

    finally:
        db.close()


def handle_prediction_event(event: dict) -> None:
    save_prediction_event(event)


def main() -> None:
    logging.basicConfig(level=logging.INFO)

    settings = get_kafka_settings()

    consumer = EventConsumer(
        topic=settings.prediction_topic,
        group_id=settings.persistence_consumer_group,
    )

    logger.info("Persistence service started.")

    consumer.consume(handle_prediction_event)


if __name__ == "__main__":
    main()