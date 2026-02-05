import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from langchain.messages import HumanMessage
from datetime import timedelta, datetime


load_dotenv()

API = "ollama"
MODEL = "llama3.2:3b"
URL = "http://localhost:11434/v1"


# Functions
def get_current_time():
    actual_time = datetime.now().strftime("%H:%M:%S")
    print(f"🔧 DEBUG: get_current_time() called, returning: {actual_time}")
    return actual_time


def get_current_date():
    return datetime.now().strftime("%Y-%m-%d")


def get_current_datetime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


function_map = {
    "get_current_time": get_current_time,
    "get_current_date": get_current_date,
    "get_current_datetime": get_current_datetime,
}

# Function Schemas
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Get current time in HH:MM:SS format",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_date",
            "description": "Get current date in YYYY-MM-DD format",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_datetime",
            "description": "Get current date and time in YYYY-MM-DD HH:MM:SS format",
            "parameters": {"type": "object", "properties": {}},
        },
    },
]


messages = [
    {
        "role": "system",
        "content": "You are a helpful assistant that helps in solving day to day problems/queries",
    },
]


def add_assistant_message(text):
    assistant_message = {"role": "assistant", "content": text}
    messages.append(assistant_message)


def add_user_message(text):
    user_message = {"role": "user", "content": text}
    messages.append(user_message)


def chat(message, tools=None):
    try:

        client = OpenAI(api_key=API, base_url=URL)
        completion = client.chat.completions.create(
            model=MODEL,
            messages=message,
            tools=tools,
        )
        # response = completion.choices[0].message.content
        return completion

    except ValueError as e:
        print(e)


print("👋 Welcome! I'm your chatbot. Type '/bye' to end the chat.\n")


def execute_tool_calls(tool_calls):
    """Execute all tool calls in a response"""
    results = []

    for tool_call in tool_calls:
        args = {}
        if tool_call.function.arguments:
            args = json.loads(tool_call.function.arguments)

        # Executing
        func_name = tool_call.function.name
        func = function_map.get(func_name)
        if func:
            try:
                result = func(**args)
                results.append({"tool_call_id": tool_call.id, "content": str(result)})
            except Exception as e:
                results.append(
                    {"tool_call_id": tool_call.id, "content": f"Error: {str(e)}"}
                )
        else:
            results.append(
                {
                    "tool_call_id": tool_call.id,
                    "content": f"Error: Function {func_name} not found",
                }
            )
    return results


def run_conversation(user_input):
    """Handling multiple conversation with multiple tool calls"""
    add_user_message(user_input)

    # while True:
    # 1st API call
    completion = chat(message=messages, tools=tools)

    if completion and hasattr(completion, "choices") and completion.choices:
        message_obj = completion.choices[0].message

        # checking wheather the response is calling a tool
        if hasattr(message_obj, "tool_calls") and message_obj.tool_calls:

            tool_call = message_obj.tool_calls[0]

            # Executing tool
            tool_results = execute_tool_calls(tool_calls=message_obj.tool_calls)

            ## Sending the function result back to the AI model
            for result in tool_results:
                # messages.append(completion.choices[0].message)
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": result["tool_call_id"],
                        "content": result["content"],
                    }
                )

            # Getting final response
            response2 = chat(message=messages, tools=tools)
            # print(f"Bot: {response2.choices[0].message.content}\n")
            add_assistant_message(response2.choices[0].message.content)
            return response2.choices[0].message.content

        else:
            if message_obj.content:
                # print(f"Bot: {completion.choices[0].message.content}\n")
                add_assistant_message(completion.choices[0].message.content)
                return completion.choices[0].message.content
            else:
                print("Bot: (No response content)\n")
    else:
        print("DEBUG: No valid response from API")


def start_chatbot():
    while True:
        user_input = input("You: ")
        if user_input.lower() == "/bye":
            print("Goodbye!")
            break

        try:
            response = run_conversation(user_input=user_input)
            print(f"Bot: {response}\n")

        except Exception as e:
            print(f"Error: {type(e).__name__}: {e}")


if __name__ == "__main__":
    start_chatbot()
