from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"
MODEL_DIR = PROJECT_ROOT / "model_artifacts"

TRAIN_PATH = DATA_DIR / "customer_churn_dataset-training-master.csv"
TEST_PATH = DATA_DIR / "customer_churn_dataset-testing-master.csv"

PIPELINE_PATH = MODEL_DIR / "churn_pipeline.joblib"
METADATA_PATH = MODEL_DIR / "model_metadata.json"

TARGET_COLUMN = "Churn"
MODEL_VERSION = "v1.0.0"

ID_COLUMNS = [
    "CustomerID",
    "CustomerId",
    "customer_id",
    "Name",
    "FullName",
    "full_name",
]