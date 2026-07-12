import numpy as np


def print_probability_diagnostics(probs, title: str) -> None:
    print(f"\n===== {title} Probability Diagnostics =====")

    print(f"Min Probability : {probs.min():.6f}")
    print(f"Max Probability : {probs.max():.6f}")
    print(f"Mean Probability: {probs.mean():.6f}")
    print(f"Std Probability : {probs.std():.6f}")

    percentiles = [0, 1, 5, 10, 25, 50, 75, 90, 95, 99, 100]

    print("\nPercentiles:")

    for p, value in zip(percentiles, np.percentile(probs, percentiles)):
        print(f"{p:>3}% : {value:.6f}")