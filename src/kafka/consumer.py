# src/kafka/consumer.py

import json
import logging
from typing import Callable

from confluent_kafka import Consumer, KafkaException

from src.kafka.config import get_kafka_settings


logger = logging.getLogger(__name__)


class EventConsumer:
    def __init__(self, topic: str, group_id: str):
        settings = get_kafka_settings()

        self.topic = topic
        self._consumer = Consumer(
            {
                "bootstrap.servers": settings.kafka_bootstrap_servers,
                "group.id": group_id,
                "auto.offset.reset": "earliest",
                "enable.auto.commit": True,
            }
        )

        self._consumer.subscribe([topic])

        logger.info(
            "Consumer subscribed to topic=%s with group_id=%s",
            topic,
            group_id,
        )

    def consume(self, handler: Callable[[dict], None]) -> None:
        """
        Continuously consume Kafka events and pass each event to handler.
        """

        try:
            while True:
                msg = self._consumer.poll(timeout=1.0)

                if msg is None:
                    continue

                if msg.error():
                    logger.warning("Kafka consumer error: %s", msg.error())
                    continue

                event = json.loads(msg.value().decode("utf-8"))

                logger.info(
                    "Consumed event_type=%s event_id=%s from topic=%s",
                    event.get("event_type"),
                    event.get("event_id"),
                    self.topic,
                )

                handler(event)

        except KeyboardInterrupt:
            logger.info("Consumer stopped manually.")

        finally:
            self.close()

    def close(self) -> None:
        logger.info("Closing Kafka consumer for topic=%s", self.topic)
        self._consumer.close()