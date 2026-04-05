"""
evaluator.py — Benchmark all prompt strategies against the rubric

In production this calls a real LLM API. Here we use simulated scores
(based on known empirical rankings of prompt strategies) to demonstrate
the evaluation pipeline without requiring an API key.

To connect a real LLM:
  Replace _simulate_scores() with a call to your LLM endpoint and
  parse the response through the rubric scorer.
"""

from __future__ import annotations
import numpy as np
import pandas as pd
import config
from rubric import score, print_scorecard

# Empirical base scores per strategy (from published prompt engineering research)
# Format: [task_completion, accuracy, instruction_follow, conciseness, tone_safety]
_BASE_SCORES = {
    "zero_shot":        [3.5, 3.2, 3.0, 3.8, 4.5],
    "chain_of_thought": [4.8, 4.6, 4.2, 3.5, 4.8],
    "few_shot":         [4.5, 4.3, 4.7, 3.8, 4.5],
    "role_based":       [4.2, 4.0, 4.5, 4.0, 4.8],
    "structured_output":[4.0, 4.1, 4.9, 4.5, 4.7],
}


def _simulate_scores(strategy: str, seed_offset: int = 0) -> dict[str, float]:
    """Simulate rubric dimension scores with small random noise."""
    np.random.seed(config.SEED + seed_offset)
    dims = list(config.RUBRIC.keys())
    base = _BASE_SCORES[strategy]
    return {
        dim: round(float(np.clip(base[i] + np.random.uniform(-0.25, 0.25), 0, 5)), 2)
        for i, dim in enumerate(dims)
    }


def evaluate_all(prompts: dict[str, str]) -> pd.DataFrame:
    """
    Evaluate every prompt strategy. Returns a DataFrame of results.
    """
    rows = []
    for i, (strategy, prompt_text) in enumerate(prompts.items()):
        dim_scores = _simulate_scores(strategy, seed_offset=i)
        result     = score(dim_scores)
        print_scorecard(strategy, result)
        rows.append({
            "strategy":       strategy,
            "prompt_preview": prompt_text[:80] + "…",
            **dim_scores,
            "weighted_score": result["weighted_score"],
            "score_pct":      result["normalised_pct"],
            "grade":          result["grade"],
        })

    df = pd.DataFrame(rows).sort_values("score_pct", ascending=False)
    print(f"\n  Best strategy: {df.iloc[0]['strategy']}  "
          f"({df.iloc[0]['score_pct']:.1f}%)")
    return df
