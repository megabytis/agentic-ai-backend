import json
import os
from dotenv import load_dotenv

load_dotenv()
from langchain.chat_models import init_chat_model
from langchain.messages import AIMessage, HumanMessage

llm = init_chat_model(
    model="gemini-2.5-flash-lite",
    model_provider="google_genai",
    temperature=0.2,
    api_key=os.getenv("GOOGLE_GEMINI_API_KEY"),
)

DATASET_PROMPT = """
You are generating test cases for evaluating a prompt.

Generate a JSON array of objects.
Each object must have a "height_cm","weight_kg","goal" & "dietary_restrictions" field

- the height_cm should include height of an Athlete in centemeter
- the weight_kg should include weight of an Athlete in kilogram
- goal should contain the goal of that athlete 
- dietary_restrictions

Generate 3 test cases only
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

    save_dataset(dataset, "dataset.json")
    print("Dataset saved.")
