"""
annotator.py — Structured annotation producer for LLM training data

Generates JSONL annotation records in the format used for:
  - Supervised fine-tuning (SFT) datasets
  - RLHF preference data
  - Model evaluation benchmarks

Output format follows the OpenAI / Anthropic annotation convention:
  {id, task_type, prompt, response, label, confidence, rubric_scores, notes}
"""

from __future__ import annotations
import json
import uuid
from datetime import datetime
import config


def make_annotation(
    strategy:    str,
    prompt:      str,
    response:    str,
    label:       str,
    confidence:  float,
    dim_scores:  dict[str, float],
    notes:       str = "",
) -> dict:
    """Build a single structured annotation record."""
    return {
        "id":           str(uuid.uuid4())[:12],
        "created_at":   datetime.utcnow().isoformat(),
        "task_type":    "sentiment_classification",
        "strategy":     strategy,
        "prompt":       prompt,
        "response":     response,
        "label":        label,
        "confidence":   round(confidence, 4),
        "rubric_scores":dim_scores,
        "annotator":    "sharath_chandra",
        "notes":        notes,
    }


def save_annotations(annotations: list[dict], path: str = None) -> None:
    """Save annotations to a JSONL file (one JSON object per line)."""
    path = path or config.ANNOTATION_FILE
    with open(path, "w") as f:
        for ann in annotations:
            f.write(json.dumps(ann) + "\n")
    print(f"  {len(annotations)} annotations saved → {path}")


def load_annotations(path: str = None) -> list[dict]:
    """Load annotations from a JSONL file."""
    path = path or config.ANNOTATION_FILE
    with open(path) as f:
        return [json.loads(line) for line in f if line.strip()]


# ── Demo responses ──────────────────────────────────────────────────────────────
DEMO_RESPONSES = {
    "zero_shot":
        "Neutral. Rate hikes signal inflation control — not directly bullish or bearish.",
    "chain_of_thought":
        "1. Subject: Central bank. 2. Signal: 'raises rates' and 'inflation' — "
        "hawkish stance. 3. Impact: Typically negative for equities, mixed for bonds. "
        "4. Sentiment: Neutral-to-Negative. Final: Neutral.",
    "few_shot":
        "Neutral",
    "role_based":
        "From a market-sentiment perspective this is a Neutral-to-Negative signal. "
        "Rate hikes tighten liquidity conditions but were priced in by the market "
        "given the inflation backdrop. Net sentiment: Neutral.",
    "structured_output":
        '{"sentiment":"Neutral","confidence":0.82,'
        '"key_signal":"raises interest rates",'
        '"reasoning":"Rate hikes are a standard inflation-control mechanism; '
        'impact is mixed and market-conditional."}',
}
