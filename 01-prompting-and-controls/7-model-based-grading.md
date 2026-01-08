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

## Model-Based Grading – Result

Outcome:

- Model returns structured evaluation (strengths, weaknesses, reasoning, score)
- Scores are persisted for later comparison

Why this matters:

- Enables objective prompt iteration
- Makes prompt quality measurable
- Allows regression detection across prompt versions

Status:

- Model-based grading implemented
- Results saved to JSON for analysis
