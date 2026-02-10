# NOTE :

'''

using tools to extract structured data (JSON) instead of prompt-based JSON extraction.

Key concept: Creating a "dummy tool" whose input schema defines our desired JSON structure. Forcing the AI to call it, then extract the arguments as our structured data.

Benefits over prompt-based JSON:
- More reliable (follows strict schema)
- No stop sequences needed
- Built-in validation via JSON schema

Use cases in your learning:
- Extract entities from text
- Parse user queries into structured commands
- Validate and normalize inputs
- Generate structured reports

'''

import json
import os
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

API = os.getenv("OPENROUTER_API_KEY")
MODEL = "stepfun/step-3.5-flash:free"
URL = "https://openrouter.ai/api/v1/"

# Function Schema
tools = []

extract_person_schema = {
    "type": "function",
    "function": {
        "name": "extract_person_info",
        "description": "Extract structured information about a person",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"},
                "email": {"type": "string"},
                "interests": {"type": "array", "items": {"type": "string"}},
            },
            "required": ["name", "age", "email"],
        },
    },
}

tools.append(extract_person_schema)

messages = [
    {
        "role": "system",
        "content": "You are a helpful assistant that helps in solving day to day problems/queries",
    },
]


def chat(message, tools=None, tool_choice=None):
    try:

        client = OpenAI(api_key=API, base_url=URL)
        params = {"model": MODEL, "messages": message}
        if tools:
            params["tools"] = tools
        if tool_choice:
            params["tool_choice"] = tool_choice

        completion = client.chat.completions.create(**params)
        return completion

    except Exception as e:
        print(f"❌ API Error: {type(e).__name__}: {e}")
        return None


user_input = "John is 30 years old, email john@example.com, likes hiking and coding"

response = chat(
    message=[{"role": "user", "content": user_input}],
    tools=[extract_person_schema],
    tool_choice={"type": "function", "function": {"name": "extract_person_info"}},
)

if response and response.choices[0].message.tool_calls:
    tool_call = response.choices[0].message.tool_calls[0]
    structured_data = json.loads(tool_call.function.arguments)
    print(structured_data)
