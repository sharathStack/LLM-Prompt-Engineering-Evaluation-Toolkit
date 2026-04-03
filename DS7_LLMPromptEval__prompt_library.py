"""
prompt_library.py — Five production-grade prompt templates

Each template follows a different prompting strategy commonly used in
LLM fine-tuning, RLHF data preparation, and model evaluation pipelines.
"""

import config

# ── Template definitions ────────────────────────────────────────────────────────
TEMPLATES = {
    "zero_shot": (
        "{instruction}\n\n"
        "Input: {input}\n\n"
        "Answer:"
    ),

    "chain_of_thought": (
        "{instruction}\n\n"
        "Think step by step before giving your final answer.\n\n"
        "Input: {input}\n\n"
        "Step-by-step reasoning:\n"
        "1. Identify the subject of the headline.\n"
        "2. Identify key economic signal words.\n"
        "3. Determine market impact direction.\n"
        "4. Conclude sentiment.\n\n"
        "Final answer:"
    ),

    "few_shot": (
        "{instruction}\n\n"
        "Examples:\n"
        "Input: Company reports record profits.\n"
        "Output: Positive\n\n"
        "Input: Firm announces mass layoffs.\n"
        "Output: Negative\n\n"
        "Input: Markets stay flat before earnings.\n"
        "Output: Neutral\n\n"
        "Now answer:\n"
        "Input: {input}\n"
        "Output:"
    ),

    "role_based": (
        "You are a senior equity analyst at a top-tier investment bank. "
        "You specialise in real-time market sentiment analysis and have 15 years "
        "of experience interpreting macroeconomic news.\n\n"
        "{instruction}\n\n"
        "Input: {input}\n\n"
        "Your analysis:"
    ),

    "structured_output": (
        "{instruction}\n\n"
        "Input: {input}\n\n"
        'Respond ONLY with a valid JSON object matching this schema exactly:\n'
        '{{\n'
        '  "sentiment": "Positive" | "Neutral" | "Negative",\n'
        '  "confidence": 0.0 to 1.0,\n'
        '  "key_signal": "the word or phrase that drove your decision",\n'
        '  "reasoning": "one sentence explanation"\n'
        '}}\n\n'
        "JSON:"
    ),
}

FEW_SHOT_EXAMPLES = (
    "Input: Company reports record profits.\nOutput: Positive\n\n"
    "Input: Firm announces mass layoffs.\nOutput: Negative\n\n"
    "Input: Markets stay flat before earnings.\nOutput: Neutral"
)


def render(strategy: str, instruction: str = None, input_text: str = None) -> str:
    """Render a prompt from a named template."""
    tpl = TEMPLATES[strategy]
    return tpl.format(
        instruction=instruction or config.TASK_INSTRUCTION,
        input=input_text or config.TASK_INPUT,
        examples=FEW_SHOT_EXAMPLES,
    )


def render_all(instruction: str = None, input_text: str = None) -> dict[str, str]:
    """Return rendered prompts for all strategies."""
    return {s: render(s, instruction, input_text) for s in config.STRATEGIES}
