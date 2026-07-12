from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class KafkaSettings(BaseSettings):
    """
    Kafka configuration loaded from environment variables.
    """

    # Kafka
    kafka_bootstrap_servers: str
    kafka_client_id: str

    # Consumer Groups
    prediction_consumer_group: str
    persistence_consumer_group: str

    # Topics
    customer_topic: str
    prediction_topic: str
    risk_topic: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


@lru_cache
def get_kafka_settings() -> KafkaSettings:
    """
    Load Kafka settings once and cache them.
    """
    return KafkaSettings()