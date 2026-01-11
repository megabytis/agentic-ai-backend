## Running the Eval (Execution Phase)

Goal:
Run a single prompt against every test case in the dataset and collect raw outputs.

Key ideas:

- Dataset = list of test cases (inputs)
- Prompt = template under test
- Eval run = dataset × prompt → outputs

Important:

- This step does NOT judge quality yet.
- No grading logic here (temporary placeholder score only).
- Outputs must be saved for later comparison.

Eval pipeline structure:

1. run_prompt(test_case) → model output
2. run_test_case(test_case) → { task, output, score }
3. run_eval(dataset) → list of results

Outcome:

- A structured JSON containing all model outputs.
- Baseline for prompt iteration and grading.
