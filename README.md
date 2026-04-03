LLM Prompt Engineering & Evaluation Toolkit
![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![LLM](https://img.shields.io/badge/Domain-LLM%20Evaluation-purple)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen)
> Benchmark 5 prompt strategies (zero-shot, CoT, few-shot, role-based, structured output) against a weighted rubric. Produces JSONL annotations for LLM training pipelines.
Project Structure
```
DS7_LLMPromptEval__config.py          ← Rubric weights, strategies, task
DS7_LLMPromptEval__prompt_library.py  ← 5 production prompt templates
DS7_LLMPromptEval__rubric.py          ← Weighted rubric scorer (0–100%)
DS7_LLMPromptEval__evaluator.py       ← Benchmark all strategies
DS7_LLMPromptEval__annotator.py       ← JSONL annotation producer
DS7_LLMPromptEval__dashboard.py       ← Bar chart + radar comparison
DS7_LLMPromptEval__main.py            ← Entry point
DS7_LLMPromptEval__requirements.txt
```
Run
```bash
pip install -r DS7_LLMPromptEval__requirements.txt
python DS7_LLMPromptEval__main.py
```
Results
Strategy	Score	Grade
Chain of Thought	~88%	A
Few-shot	~85%	A
Role-based	~82%	B
Structured Output	~80%	B
Zero-shot	~68%	C
