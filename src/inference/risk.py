# src/inference/risk.py


def get_risk_level(probability: float) -> str:
    """
    Convert churn probability into a risk level.
    """

    if probability < 0.35:
        return "LOW"

    if probability < 0.65:
        return "MEDIUM"

    return "HIGH"


def get_risk_transition(
    previous_risk: str | None,
    current_risk: str,
) -> str:
    """
    Determine the transition between two risk levels.
    """

    if previous_risk is None:
        return "INITIAL"

    if previous_risk == current_risk:
        return "NO_CHANGE"

    return f"{previous_risk}_TO_{current_risk}"