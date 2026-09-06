#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    with (ROOT / "results" / "manuscript_summary_snapshot.csv").open(
        encoding="utf-8"
    ) as handle:
        rows = list(csv.DictReader(handle))
    methods = [row["method"] for row in rows]
    ranks = [float(row["average_rank"]) for row in rows]
    order = sorted(range(len(rows)), key=lambda i: ranks[i])
    fig, ax = plt.subplots(figsize=(7.2, 4.2), constrained_layout=True)
    ax.barh([methods[i] for i in order][::-1], [ranks[i] for i in order][::-1])
    ax.set_xlabel("Average rank (lower is better)")
    ax.grid(axis="x", alpha=0.25)
    (ROOT / "figures").mkdir(exist_ok=True)
    fig.savefig(ROOT / "figures" / "Fig3_rebuilt.pdf")
    fig.savefig(ROOT / "figures" / "Fig3_rebuilt.png", dpi=600)
    plt.close(fig)

    budgets = [10, 25, 50, 100]
    accuracies = [66.94, 73.89, 75.90, 80.35]
    fig, ax = plt.subplots(figsize=(6.4, 3.8), constrained_layout=True)
    ax.plot(budgets, accuracies, marker="o", linewidth=2)
    ax.set(xlabel="Training-label budget (%)", ylabel="Mean accuracy (%)")
    ax.set_xticks(budgets)
    ax.grid(alpha=0.25)
    fig.savefig(ROOT / "figures" / "Fig4_rebuilt.pdf")
    fig.savefig(ROOT / "figures" / "Fig4_rebuilt.png", dpi=600)
    plt.close(fig)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

