import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

from src.training.config import TARGET_COLUMN, ID_COLUMNS


def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = df.dropna()

    for col in ID_COLUMNS:
        if col in df.columns:
            df = df.drop(col, axis=1)

    return df


def split_features_target(df: pd.DataFrame):
    X = df.drop(TARGET_COLUMN, axis=1)
    y = df[TARGET_COLUMN]

    if y.dtype == "object":
        y = y.map(
            {
                "Yes": 1,
                "No": 0,
                "yes": 1,
                "no": 0,
                "True": 1,
                "False": 0,
                "true": 1,
                "false": 0,
            }
        )

    return X, y


def build_preprocessor(X: pd.DataFrame) -> ColumnTransformer:
    numeric_features = X.select_dtypes(
        include=["int64", "float64"]
    ).columns.tolist()

    categorical_features = X.select_dtypes(
        include=["object", "string", "category", "bool"]
    ).columns.tolist()

    preprocessor = ColumnTransformer(
        transformers=[
            ("categorical", OneHotEncoder(handle_unknown="ignore"), categorical_features),
            ("numeric", "passthrough", numeric_features),
        ]
    )

    return preprocessor