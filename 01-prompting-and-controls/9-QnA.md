## Understanding Evaluation Needs

### Why do you think it's important to have an objective evaluation process when you're trying to improve AI prompts?

- evaluation helps to let us know how effective our prompt is !
- we got some score from model to know the effectiveness of prompt based on the outputs of the tasks
- "Objective" in this context means relying on facts, measurable criteria, and unbiased assessment, rather than personal feelings or interpretations.
- so, relying on feelings i.e. if we'll score based on feeling by ourselves, then it can lead to random or inconsistent scoring, while measurable standards allow a model to properly understand and evaluate the output. This consistency and clarity are exactly what makes objective evaluation so powerful for improving prompts.

## Code-based Grading

### This approach uses custom code to evaluate model outputs. Can you think of a scenario where a code-based grader would be particularly useful for checking the correctness of an AI's output?

- yeah code-based grading also can be called as syntax-grading
- i will check the proper format of the outputs wheather the output is in proper JSON/regex/PYTHON or whatever , it shouldn' consist anything else, pura synatx. That's code based grading

### Can you give me a specific example of a task where validating the output format using a code-based grader would be critical for the AI's performance or usability?

- e.g.: "task": "Write a Python function that takes a list of integers and returns a new list containing only the even numbers."

- If the AI is supposed to generate a Python function, a code-based grader could check if the output is indeed valid Python syntax, if it defines a function, and even if the function signature matches what was requested. This ensures the generated code is immediately usable.

## Model-based Grading

### While code-based grading is excellent for objective checks like syntax, model-based grading uses another AI model to assess the quality of outputs. In what kinds of situations would you use a model-based grader instead of, or in addition to, a code-based grader?

- When i don't need output in machine-readable format like json/regex/python or something like that, code-based graders won't be helpful.
- But Model-based grader shines when we just need output as a simple text-based answer

### Can you think of an example of a prompt where the expected output is a "simple text-based answer" that would require a model-based grader to evaluate its quality, rather than just its format?

- prompt: Please solve the following task:
- "task": "Write a Python function that takes a list of integers and returns a new list containing only the even numbers. and teach me each step line by line, no proper python format needed ",

- In this case, the user explicitly states "no proper python format needed" and asks for a line-by-line explanation. A code-based grader would fail here because it's looking for strict syntax, which isn't the primary goal. A model-based grader, however, could evaluate the quality of the explanation: Is it clear? Is it accurate? Does it teach effectively, line by line? It can assess these more subjective criteria.

## Test Dataset Creation

### Why is it important to create a diverse and comprehensive test dataset when evaluating prompts, and what kind of elements should such a dataset include?

- it is very important to create a dataset by using a model to generate mutiple outputs based on our one prompt to check how effective our prompt is towards multiple tasks, then it would be helpful to give score
- we should include very wide range very different type of challenging questions to test the effectveness of our prompt
- elements like 'task', ''format' & 'solution_criteria' can be included in dataset

## Analyzing Results and Iteration

### Beyond just the scores, what else would you look for in the results to understand why a prompt might be performing well or poorly? How do you use that understanding to make specific, targeted improvements to the prompt itself?

- i can add another field named 'reasoning' on output json file, especially from a model-based grader to get to know where the solution failed or succeeded nd how, the resoning tells everything
