from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report,
    roc_auc_score,
    average_precision_score,
    log_loss,
    brier_score_loss,
)

from src.training.diagnostics import print_probability_diagnostics


def evaluate_model(model, X, y, title: str):
    y_pred = model.predict(X)
    y_proba = model.predict_proba(X)[:, 1]

    metrics = {
        "accuracy": accuracy_score(y, y_pred),
        "roc_auc": roc_auc_score(y, y_proba),
        "pr_auc": average_precision_score(y, y_proba),
        "log_loss": log_loss(y, y_proba),
        "brier_score": brier_score_loss(y, y_proba),
    }

    print(f"\n{'=' * 25}")
    print(title)
    print(f"{'=' * 25}")

    print("\nTarget Distribution:")
    print(y.value_counts())
    print(y.value_counts(normalize=True))

    print("\nAccuracy:")
    print(metrics["accuracy"])

    print("\nConfusion Matrix:")
    print(confusion_matrix(y, y_pred))

    print("\nClassification Report:")
    print(classification_report(y, y_pred))

    print("\nROC AUC :", metrics["roc_auc"])
    print("PR AUC  :", metrics["pr_auc"])
    print("Log Loss:", metrics["log_loss"])
    print("Brier   :", metrics["brier_score"])

    print_probability_diagnostics(y_proba, title)

    return metrics