"""
config.py — LLM Prompt Engineering & Evaluation Toolkit
"""

# ── Task ────────────────────────────────────────────────────────────────────────
TASK_INSTRUCTION = (
    "Classify the sentiment of the following financial news headline "
    "as Positive, Neutral, or Negative."
)
TASK_INPUT = "Central bank raises interest rates amid inflation concerns."

# ── Prompt strategies ───────────────────────────────────────────────────────────
STRATEGIES = [
    "zero_shot",
    "chain_of_thought",
    "few_shot",
    "role_based",
    "structured_output",
]

# ── Rubric weights (must sum to 1.0) ────────────────────────────────────────────
RUBRIC = {
    "task_completion":    {"weight": 0.30, "max": 5,
                           "desc": "Does the response fully address the task?"},
    "accuracy":           {"weight": 0.25, "max": 5,
                           "desc": "Are facts and reasoning correct?"},
    "instruction_follow": {"weight": 0.20, "max": 5,
                           "desc": "Does it follow format and constraints?"},
    "conciseness":        {"weight": 0.15, "max": 5,
                           "desc": "Is it appropriately brief?"},
    "tone_safety":        {"weight": 0.10, "max": 5,
                           "desc": "Appropriate tone; no harmful content?"},
}

# ── Simulation seed ─────────────────────────────────────────────────────────────
SEED = 42

# ── Output ──────────────────────────────────────────────────────────────────────
ANNOTATION_FILE  = "annotations.jsonl"
CHART_OUTPUT     = "prompt_eval_dashboard.png"
CHART_DPI        = 150
