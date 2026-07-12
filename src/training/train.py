import joblib
import pandas as pd

from xgboost import XGBClassifier

from sklearn.pipeline import Pipeline

from src.training.config import (
    TRAIN_PATH,
    TEST_PATH,
    MODEL_DIR,
    PIPELINE_PATH,
)

from src.training.preprocess import (
    preprocess_data,
    split_features_target,
    build_preprocessor,
)

from src.training.evaluate import evaluate_model
from src.training.metadata import save_metadata


def load_data():
    train_df = pd.read_csv(TRAIN_PATH)
    test_df = pd.read_csv(TEST_PATH)
    return train_df, test_df


def calculate_scale_pos_weight(y_train):
    negative_count = (y_train == 0).sum()
    positive_count = (y_train == 1).sum()

    if positive_count == 0:
        return 1

    return negative_count / positive_count


def build_model(scale_pos_weight):
    return XGBClassifier(
        n_estimators=300,
        learning_rate=0.03,
        max_depth=3,
        min_child_weight=10,
        subsample=0.8,
        colsample_bytree=0.8,
        reg_alpha=1.0,
        reg_lambda=10.0,
        scale_pos_weight=scale_pos_weight,
        random_state=42,
        eval_metric="logloss",
    )


def main():
    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    train_df, test_df = load_data()

    print("Raw Train Shape:", train_df.shape)
    print("Raw Test Shape :", test_df.shape)

    train_df = preprocess_data(train_df)
    test_df = preprocess_data(test_df)

    print("Processed Train Shape:", train_df.shape)
    print("Processed Test Shape :", test_df.shape)

    X_train, y_train = split_features_target(train_df)
    X_test, y_test = split_features_target(test_df)

    preprocessor = build_preprocessor(X_train)

    scale_pos_weight = calculate_scale_pos_weight(y_train)
    print("\nScale Pos Weight:", scale_pos_weight)

    model = build_model(scale_pos_weight)

    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", model),
        ]
    )

    print("\nTraining pipeline...\n")
    pipeline.fit(X_train, y_train)

    joblib.dump(pipeline, PIPELINE_PATH)

    print("\nPipeline saved successfully!")
    print(PIPELINE_PATH)

    train_metrics = evaluate_model(
        pipeline,
        X_train,
        y_train,
        "TRAIN SET",
    )

    test_metrics = evaluate_model(
        pipeline,
        X_test,
        y_test,
        "TEST SET",
    )

    save_metadata(
        model_name="XGBoost",
        train_rows=len(train_df),
        test_rows=len(test_df),
        features=X_train.columns.tolist(),
        train_metrics=train_metrics,
        test_metrics=test_metrics,
    )


if __name__ == "__main__":
    main()