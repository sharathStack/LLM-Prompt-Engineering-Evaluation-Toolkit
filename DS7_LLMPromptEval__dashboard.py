"""
dashboard.py — Prompt evaluation comparison: bar chart + radar chart
"""
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import pandas as pd
import config

COLORS = ["#3498db", "#e74c3c", "#2ecc71", "#f39c12", "#9b59b6"]
DIMS   = list(config.RUBRIC.keys())


def plot(results_df: pd.DataFrame) -> None:
    fig = plt.figure(figsize=(16, 7))
    fig.suptitle("LLM Prompt Strategy Evaluation — Rubric Scoring",
                 fontsize=13, fontweight="bold")
    gs = gridspec.GridSpec(1, 2, figure=fig, wspace=0.40)

    # ── 1. Horizontal bar: normalised score ───────────────────────────────────
    ax1 = fig.add_subplot(gs[0])
    strategies = results_df["strategy"].tolist()
    scores     = results_df["score_pct"].tolist()
    grades     = results_df["grade"].tolist()
    bar_cols   = [COLORS[i % len(COLORS)] for i in range(len(strategies))]

    bars = ax1.barh(strategies, scores, color=bar_cols, alpha=0.85, height=0.55)
    ax1.axvline(80, color="gray", linestyle="--", alpha=0.55, label="80% threshold")
    ax1.set_xlim(0, 105)
    ax1.set_xlabel("Normalised Score (%)", fontsize=10)
    ax1.set_title("Strategy Comparison — Overall Score", fontweight="bold")
    ax1.legend(fontsize=9)
    ax1.invert_yaxis()
    for bar, sc, grade in zip(bars, scores, grades):
        ax1.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height() / 2,
                 f"{sc:.1f}%  ({grade})", va="center", fontsize=9)

    # ── 2. Radar chart: top-3 strategies ─────────────────────────────────────
    ax2 = fig.add_subplot(gs[1], projection="polar")
    n_dim  = len(DIMS)
    angles = [i / n_dim * 2 * math.pi for i in range(n_dim)] + [0]

    top3 = results_df.head(3)
    for i, (_, row) in enumerate(top3.iterrows()):
        vals   = [row[d] for d in DIMS] + [row[DIMS[0]]]
        label  = row["strategy"].replace("_", " ").title()
        ax2.plot(angles, vals, linewidth=2.0, color=COLORS[i], label=label)
        ax2.fill(angles, vals, alpha=0.08, color=COLORS[i])

    ax2.set_xticks(angles[:-1])
    ax2.set_xticklabels([d.replace("_", "\n") for d in DIMS], size=8)
    ax2.set_ylim(0, 5)
    ax2.set_title("Top-3 Strategies — Rubric Radar", fontweight="bold", pad=18)
    ax2.legend(loc="upper right", bbox_to_anchor=(1.35, 1.12), fontsize=8)

    plt.tight_layout()
    plt.savefig(config.CHART_OUTPUT, dpi=config.CHART_DPI, bbox_inches="tight")
    plt.close()
    print(f"Dashboard saved → {config.CHART_OUTPUT}")
