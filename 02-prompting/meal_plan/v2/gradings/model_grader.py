import os
import json
from dotenv import load_dotenv

load_dotenv()
from google import genai


def chat(message, stop_sequence="```"):
    try:
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite", contents=f"{message}"
        )
        # print(f"Response: \n{response}")
        return response.text
    except ValueError as e:
        print(e)


def grade_by_model(test_cases_list, outputs_list):
    eval_text = []

    for i in range(len(test_cases_list)):
        test_case = test_cases_list[i]
        output_item = outputs_list[i]

        grading_prompt = f"""
You are an expert AWS code reviewer. Your task is to evaluate the following AI-generated solution.

Original Task:
<task>
{test_case}
</task>

Solution to Evaluate:
<solution>
{output_item["output"]}
</solution>

Output Format
Provide your evaluation as a structured JSON object with the following fields, in this specific order:
- "strengths": An array of 1-2 key strengths
- "weaknesses": An array of 1-2 key areas for improvement
- "reasoning": A concise explanation of your overall assessment
- "score": A number between 1-10

Respond with JSON. Keep your response concise and direct.
Example response shape:
{{
    "strengths": string[],
    "weaknesses": string[],
    "reasoning": string,
    "score": number
}}
    """

        messages = []
        messages.append({"role": "user", "content": grading_prompt})
        messages.append({"role": "assistant", "content": "```json"})

        result = chat(messages, stop_sequence="```")
        cleaned_result = result.replace("```json", "").replace("```", "").strip()
        print(f"Cleaned result content: {repr(cleaned_result)}")

        if cleaned_result.startswith("'") and cleaned_result.endswith("'"):
            cleaned_result = cleaned_result[1:-1]

        cleaned_result = cleaned_result.replace("\\'", "'")

        parsed_result = json.loads(cleaned_result)
        eval_text.append(parsed_result)

        def save_eval_text(eval_text, path="v2/gradings/model_gradings_v2.json"):
            with open(path, "w") as f:
                json.dump(eval_text, f, indent=2)

        save_eval_text(eval_text)
    return eval_text


with open("dataset.json", "r") as f:
    test_cases = json.load(f)

with open("v2/outputs_v2.json", "r") as f:
    outputs = json.load(f)

grade = grade_by_model(test_cases, outputs)
