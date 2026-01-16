import json
import os
from dotenv import load_dotenv

load_dotenv()
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage, AIMessage

llm = init_chat_model(
    model="google/gemma-3-27b-it:free",
    model_provider="google",
    api_key=API,
    base_url="https://openrouter.ai/api/v1",
)


def load_prompt(path="v2/prompt_v2.txt"):
    with open(path, "r") as f:
        return f.read()


def load_dataset(path="dataset.json"):
    with open(path, "r") as f:
        return json.load(f)


def run_prompt(prompt_template, test_case):
    prompt = (
        prompt_template.replace("{{height_cm}}", str(test_case["height_cm"]))
        .replace("{{weight_kg}}", str(test_case["weight_kg"]))
        .replace("{{goal}}", test_case["goal"])
        .replace("{{dietary_restrictions}}", test_case["dietary_restrictions"])
    )

    message = [HumanMessage(content=prompt)]
    response = llm.invoke(message)

    return response.content


def run_test_case(prompt_template, test_case):
    output = run_prompt(prompt_template, test_case)

    return {"credentials": test_case, "output": output, "score": 10}


def run_eval(dataset, pompt_template):
    results = []

    for test_case in dataset:
        result = run_test_case(prompt_template, test_case)
        results.append(result)

    return results


if __name__ == "__main__":
    prompt_template = load_prompt()
    dataset = load_dataset()

    results = run_eval(dataset, prompt_template)

    with open("v2/outputs_v2.json", "w") as f:
        json.dump(results, f, indent=2)

    print("Eval complete. Results saved to outputs_v1.json")
