import joblib

from src.training.config import PIPELINE_PATH


_pipeline = None


def load_pipeline():
    global _pipeline

    if _pipeline is None:
        if not PIPELINE_PATH.exists():
            raise FileNotFoundError(f"Model pipeline not found: {PIPELINE_PATH}")

        _pipeline = joblib.load(PIPELINE_PATH)

    return _pipeline