# src/kafka/producer.py

from functools import lru_cache
import json
import logging

from confluent_kafka import Producer

from src.kafka.config import get_kafka_settings


logger = logging.getLogger(__name__)


class EventProducer:
    def __init__(self):
        settings = get_kafka_settings()

        self._producer = Producer(
            {
                "bootstrap.servers": settings.kafka_bootstrap_servers,
                "client.id": settings.kafka_client_id,
            }
        )

    @staticmethod
    def _delivery_report(err, msg):
        if err is not None:
            logger.error("Event delivery failed: %s", err)
        else:
            logger.info(
                "Event delivered to topic=%s partition=%s offset=%s",
                msg.topic(),
                msg.partition(),
                msg.offset(),
            )

    def publish(self, topic: str, event) -> None:
        event_dict = event.model_dump(mode="json", by_alias=True)
        event_json = json.dumps(event_dict)

        logger.info(
            "Publishing event_type=%s event_id=%s to topic=%s",
            event_dict.get("event_type"),
            event_dict.get("event_id"),
            topic,
        )

        self._producer.produce(
            topic=topic,
            value=event_json.encode("utf-8"),
            callback=self._delivery_report,
        )

        self._producer.poll(0)
        self._producer.flush()


@lru_cache
def get_event_producer() -> EventProducer:
    return EventProducer()