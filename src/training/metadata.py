import json

import sklearn
import xgboost

from src.training.config import METADATA_PATH, MODEL_VERSION


def save_metadata(
    model_name: str,
    train_rows: int,
    test_rows: int,
    features: list,
    train_metrics: dict,
    test_metrics: dict,
) -> None:
    metadata = {
        "model_name": model_name,
        "model_version": MODEL_VERSION,
        "train_rows": train_rows,
        "test_rows": test_rows,
        "feature_count": len(features),
        "features": features,
        "train_metrics": train_metrics,
        "test_metrics": test_metrics,
        "library_versions": {
            "scikit_learn": sklearn.__version__,
            "xgboost": xgboost.__version__,
        },
    }

    with open(METADATA_PATH, "w") as f:
        json.dump(metadata, f, indent=4)

    print("\nModel metadata saved.")
    print(METADATA_PATH)