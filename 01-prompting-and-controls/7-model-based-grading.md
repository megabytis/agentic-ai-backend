## Model-Based Grading

What:
Use a second LLM call to evaluate the quality of the original model’s output.

Why:
Some qualities cannot be validated with code:

- Task correctness
- Completeness
- Logical accuracy
- Instruction-following

How:

- Feed the original task + model output into a grading prompt
- Ask the grader model for:
  - strengths
  - weaknesses
  - reasoning
  - numeric score (1–10)

Key Insight:
Prompt evaluation itself is an LLM-powered system.
LLMs can judge other LLMs when guided correctly.
