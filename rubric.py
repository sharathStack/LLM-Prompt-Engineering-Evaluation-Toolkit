"""
rubric.py — Weighted rubric scoring engine

Used by AI/LLM annotators (human or automated) to score model responses
across multiple quality dimensions. Produces a normalised 0–100 quality score.

Rubric dimensions (from config.RUBRIC):
  task_completion    (30%) — Did the model do what was asked?
  accuracy           (25%) — Are facts and logic correct?
  instruction_follow (20%) — Did it respect format constraints?
  conciseness        (15%) — Was it appropriately brief?
  tone_safety        (10%) — Was tone appropriate and content safe?
"""

from __future__ import annotations
import config


def score(dimension_scores: dict[str, float]) -> dict:
    """
    Compute weighted total score from per-dimension scores.

    Args:
        dimension_scores: {dim_name: score_0_to_5}

    Returns:
        {
            "dimension_scores":  original input,
            "weighted_score":    float (0–5 scale),
            "normalised_pct":    float (0–100),
            "grade":             letter grade A/B/C/D/F
        }
    """
    max_possible = sum(
        v["max"] * v["weight"] for v in config.RUBRIC.values()
    )
    weighted = sum(
        dimension_scores.get(dim, 0) * config.RUBRIC[dim]["weight"]
        for dim in config.RUBRIC
    )
    pct = round(100 * weighted / max_possible, 1)

    grade = (
        "A" if pct >= 85 else
        "B" if pct >= 70 else
        "C" if pct >= 55 else
        "D" if pct >= 40 else "F"
    )

    return {
        "dimension_scores": dimension_scores,
        "weighted_score":   round(weighted, 3),
        "normalised_pct":   pct,
        "grade":            grade,
    }


def print_scorecard(strategy: str, result: dict) -> None:
    """Pretty-print a rubric scorecard to terminal."""
    print(f"\n  {'─'*42}")
    print(f"  Strategy : {strategy.upper().replace('_', ' ')}")
    print(f"  Grade    : {result['grade']}  ({result['normalised_pct']:.1f}%)")
    print(f"  {'Dimension':<22} {'Score':>5}  {'Weight':>7}")
    print(f"  {'─'*38}")
    for dim, val in result["dimension_scores"].items():
        w = config.RUBRIC[dim]["weight"]
        print(f"  {dim:<22} {val:>5.2f}  ({w:.0%})")
