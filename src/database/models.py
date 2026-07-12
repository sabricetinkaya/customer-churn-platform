from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.database import Base


class Customer(Base):
    __tablename__ = "customer_information"

    customer_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    gender: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    tenure: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    usage_frequency: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    support_calls: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    payment_delay: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    subscription_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    contract_length: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    total_spend: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    last_interaction: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    current_prediction: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    current_churn_probability: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    current_risk_level: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )

    prediction_history: Mapped[list["PredictionHistory"]] = relationship(
        back_populates="customer",
        cascade="all, delete-orphan",
    )


class PredictionHistory(Base):
    __tablename__ = "prediction_history"

    prediction_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customer_information.customer_id"),
        nullable=False,
        index=True,
    )

    churn_probability: Mapped[float] = mapped_column(Float, nullable=False)
    predicted_churn: Mapped[bool] = mapped_column(Boolean, nullable=False)
    risk_level: Mapped[str] = mapped_column(String(20), nullable=False)

    previous_risk_level: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    risk_transition: Mapped[str] = mapped_column(String(50), nullable=False)

    model_version: Mapped[str] = mapped_column(String(50), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )

    customer: Mapped["Customer"] = relationship(
        back_populates="prediction_history",
    )