## Code-Based Grading (Syntax + Format Validation)

Goal:
Ensure the model output:

1. Contains ONLY code (Python / JSON / RegEx)
2. Has valid syntax for the expected format

Why this matters:

- Model graders judge quality but cannot enforce rules
- Code graders enforce hard constraints
- Prevents hallucinated explanations, comments, or invalid code

Approach:

- Each test case defines an expected `format`
- Output is validated using language-native parsers
- Syntax success → score = 10
- Syntax failure → score = 0
