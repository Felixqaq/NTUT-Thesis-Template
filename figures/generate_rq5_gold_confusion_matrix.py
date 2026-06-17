"""Regenerate the RQ5 GOLD four-class confusion matrix figure.

Plots the total (5-fold aggregated) confusion matrix of the
TAP-CT-S-3D late fusion model (focal loss, gamma=1) used in Table 4.10 /
Figure 4.4. GOLD 1 validation patients are reused across folds, so the
GOLD 1 row sums to 5 test predictions.
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

OUT = Path(__file__).resolve().with_name("total_confusion_matrix.png")

# TAP-CT-S-3D late fusion (focal gamma=1), aggregated over 5 folds.
# Rows = true label, cols = predicted label; order: GOLD 1..4.
cm = np.array([
    [0, 2, 2, 1],
    [1, 8, 0, 2],
    [0, 2, 10, 1],
    [0, 3, 2, 1],
])
labels = ["GOLD 1", "GOLD 2", "GOLD 3", "GOLD 4"]


def main() -> None:
    plt.rcParams["font.family"] = "DejaVu Sans"
    fig, ax = plt.subplots(figsize=(8.4, 7.2))
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        cbar_kws={"label": "Count"},
        annot_kws={"size": 28},
        xticklabels=labels,
        yticklabels=labels,
        square=False,
        linewidths=0,
        ax=ax,
    )
    ax.set_xlabel("Predicted Label", fontsize=20, fontweight="bold")
    ax.set_ylabel("True Label", fontsize=20, fontweight="bold")
    ax.tick_params(axis="x", labelsize=16, rotation=0)
    ax.tick_params(axis="y", labelsize=16, rotation=90)
    cbar = ax.collections[0].colorbar
    cbar.ax.set_ylabel("Count", fontsize=16)
    cbar.ax.tick_params(labelsize=13)
    fig.tight_layout()
    fig.savefig(OUT, dpi=200, bbox_inches="tight")
    print(OUT)


if __name__ == "__main__":
    main()
