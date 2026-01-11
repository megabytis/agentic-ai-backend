from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()


API = os.getenv("OPENROUTER_API_KEY")
MODEL = "qwen/qwen3-coder:free"

messages = [
    {
        "role": "system",
        "content": "You are a helpful assistant that explains concepts clearly and concisely.",
    }
]


def add_assistant_message(text):
    assistant_message = {"role": "assistant", "content": text}
    messages.append(assistant_message)


def add_user_message(text):
    user_message = {"role": "user", "content": text}
    messages.append(user_message)


def chat(message):
    try:
        llm = ChatOpenAI(
            api_key=API,
            base_url="https://openrouter.ai/api/v1",
            model=MODEL,
        )
        response = llm.invoke(message)
        return response.content
    except ValueError as e:
        print(e)


print("👋 Welcome! I'm your chatbot. Type '/bye' to end the chat.\n")


def start_chatbot():
    while True:
        user_input = input("You: ")
        if user_input.lower() == "/bye":
            print("Goodbye!")
            break

        try:
            add_user_message(user_input)
            response = chat(messages)
            print(f"Bot: {response}\n")
            add_assistant_message(response)
        except ValueError as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    start_chatbot()
