import pandas as pd

from src.inference.model_loader import load_pipeline
from src.inference.risk import get_risk_level
from src.training.config import MODEL_VERSION


DROP_COLUMNS = [
    "CustomerID",
    "CustomerId",
    "customer_id",
    "full_name",
    "FullName",
    "Name",
]


def preprocess_customer(customer_data: dict) -> pd.DataFrame:
    df = pd.DataFrame([customer_data])

    for col in DROP_COLUMNS:
        if col in df.columns:
            df = df.drop(col, axis=1)

    return df


def predict_customer(customer_data: dict) -> dict:
    pipeline = load_pipeline()

    customer_id = (
        customer_data.get("customer_id")
        or customer_data.get("CustomerID")
        or customer_data.get("CustomerId")
    )

    X = preprocess_customer(customer_data)

    prediction = pipeline.predict(X)[0]
    probability = pipeline.predict_proba(X)[0][1]
    risk_level = get_risk_level(float(probability))

    return {
        "customer_id": customer_id,
        "predicted_churn": bool(prediction),
        "churn_probability": float(probability),
        "risk_level": risk_level,
        "model_version": MODEL_VERSION,
    }


if __name__ == "__main__":
    sample_customer = {
        "customer_id": 101,
        "Age": 45,
        "Gender": "Male",
        "Tenure": 5,
        "Usage Frequency": 2,
        "Support Calls": 10,
        "Payment Delay": 15,
        "Subscription Type": "Basic",
        "Contract Length": "Monthly",
        "Total Spend": 200,
        "Last Interaction": 20,
    }

    print(predict_customer(sample_customer))