"""
main.py — LLM Prompt Engineering & Evaluation Toolkit entry point
"""
import config
from prompt_library import render_all
from evaluator      import evaluate_all
from annotator      import (make_annotation, save_annotations,
                            DEMO_RESPONSES)
from dashboard      import plot


def main():
    print("=" * 55)
    print("  LLM PROMPT ENGINEERING & EVALUATION TOOLKIT")
    print("=" * 55)

    # 1. Render all prompt variants
    print(f"\n[1] Rendering {len(config.STRATEGIES)} prompt strategies...")
    prompts = render_all()
    for strat, prompt in prompts.items():
        print(f"\n  ── {strat.upper()} ──")
        print(f"  {prompt[:130]}...")

    # 2. Evaluate against rubric
    print("\n[2] Scoring each strategy against rubric...")
    results_df = evaluate_all(prompts)

    print("\n  ── Ranking Summary ──────────────────────────────")
    print(results_df[["strategy", "score_pct", "grade"]].to_string(index=False))

    # 3. Build annotation records
    print("\n[3] Producing structured annotations (JSONL)...")
    annotations = []
    for i, (strat, prompt) in enumerate(prompts.items()):
        row  = results_df[results_df["strategy"] == strat].iloc[0]
        dims = {d: row[d] for d in config.RUBRIC}
        ann  = make_annotation(
            strategy   = strat,
            prompt     = prompt,
            response   = DEMO_RESPONSES.get(strat, ""),
            label      = "neutral",
            confidence = round(row["score_pct"] / 100, 4),
            dim_scores = dims,
            notes      = f"Grade {row['grade']} — {strat} strategy",
        )
        annotations.append(ann)
    save_annotations(annotations)

    # 4. Dashboard
    print("\n[4] Generating evaluation dashboard...")
    plot(results_df)

    print("\n  Done ✓")


if __name__ == "__main__":
    main()
