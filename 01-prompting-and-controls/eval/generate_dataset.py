import json
import os
from dotenv import load_dotenv
load_dotenv()
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage, AIMessage

llm = init_chat_model(
    model="gemini-2.5-flash-lite",
    model_provider="google_genai",
    temperature=0.2,
    api_key=os.getenv("GEMINI_API_KEY"),
)

DATASET_PROMPT = """
You are generating test cases for evaluating a prompt.

Generate a JSON array of objects.
Each object must have a "task" field.

The task should ask for ONE of the following outputs:
- Python code
- JSON configuration
- A regular expression

Do NOT include explanations.
Return ONLY valid JSON.
Generate exactly 3 tasks.
"""


def generate_dataset():
    messages = [HumanMessage(content=DATASET_PROMPT), AIMessage(content="```json")]

    response = llm.invoke(messages, stop=["```"])

    raw_json = response.content.strip()
    return json.loads(raw_json)


def save_dataset(dataset, path="dataset.json"):
    with open(path, "w") as f:
        json.dump(dataset, f, indent=2)


if __name__ == "__main__":
    dataset = generate_dataset()
    print("Generated dataset: ")
    print(dataset)

    save_dataset(dataset,'tasks.json')
    print("Saved dataset.json")
