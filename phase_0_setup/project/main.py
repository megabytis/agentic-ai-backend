import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from shared.config import GEMINI_API_KEY, DEFAULT_MODEL
from google import genai


def call_llm(user_message: str) -> dict:
    """
    calls gemini API with a user message.
    Returns response text and token usage.
    """
    client = genai.Client(api_key=GEMINI_API_KEY)
    response = client.models.generate_content(
        model=DEFAULT_MODEL, contents=user_message
    )

    # Extracting token usage
    usage = response.usage_metadata

    return {"response": response.text,"usage":{
        "input_tokens": usage.prompt_token_count,
        "output_tokens":usage.candidates_token_count,
        "total_tokens":usage.total_token_count
    }}


def main():
    user_input = input("Enter your nessage: ")
    result=call_llm(user_input)

    print("\n=== Response ===")
    print(result['response'])

    print("\n=== Token Usage ===")
    print(f"Input tokens: {result['usage']['input_tokens']}")
    print(f"Output tokens: {result['usage']['output_tokens']}")
    print(f"Total tokens: {result['usage']['total_tokens']}")


if __name__ == "__main__":
    main()
