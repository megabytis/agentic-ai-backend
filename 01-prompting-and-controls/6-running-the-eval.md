## Prompt Evaluation – Running the Eval

Goal:
Evaluate how well a prompt performs across multiple test cases.

Core idea:
For each test case:

1. Merge test input with the prompt
2. Send to LLM
3. Capture output
4. Grade the output
5. Store everything for analysis

Eval Pipeline Structure:
dataset → run_prompt → run_test_case → run_eval → outputs.json

Key takeaway:
Prompt quality must be measured systematically, not guessed.
