"""Regenerate the RQ4 AC three-class confusion matrix figure.

Plots the total (5-fold aggregated) confusion matrix of the
TAP-CT-S-3D late fusion model used in Table 4.9 / Figure 4.x.
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

OUT = Path(__file__).resolve().with_name("rq4_ac_3class_confusion_matrix.png")

# TAP-CT-S-3D late fusion, aggregated over 5 folds.
# Rows = true label, cols = predicted label; order: Abnormal, Intermediate, Normal.
cm = np.array([
    [9, 1, 4],
    [0, 0, 5],
    [2, 1, 44],
])
labels = ["Abnormal", "Intermediate", "Normal"]


def main() -> None:
    plt.rcParams["font.family"] = "DejaVu Sans"
    fig, ax = plt.subplots(figsize=(9, 7.2))
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        cbar_kws={"label": "Count"},
        annot_kws={"size": 30},
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
