## Prompt Evaluation – Generating Test Datasets

Goal:
Evaluate whether a prompt consistently produces outputs in one of the allowed formats:

- Python
- JSON configuration
- Regular expression

Key ideas:

- Prompt quality must be tested across many inputs, not one-off examples.
- A dataset = list of inputs we repeatedly test against the same prompt.
- Datasets can be:
  - Hand-written (small, controlled)
  - LLM-generated (scalable)

Why generate datasets with an LLM:

- Faster coverage
- Diverse edge cases
- Cheap models (e.g. Haiku) are sufficient

Important constraint:

- LLM output must be **machine-parseable** (pure JSON).
- Use stop sequences / prefill to enforce structure.

Output of this step:

- A JSON file containing tasks to evaluate the prompt against.
