import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from langchain.messages import HumanMessage
from datetime import timedelta, datetime
import random


load_dotenv()

API = os.getenv("OPENROUTER_API_KEY")
MODEL = "openai/gpt-oss-120b:free"
URL = "https://openrouter.ai/api/v1/"

# Functions
def get_current_time():
    return datetime.now().strftime("%H:%M:%S")


def get_current_date():
    return datetime.now().strftime("%Y-%m-%d")


def get_current_datetime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def add_duration_to_datetime(base_datetime: str, duration: str) -> str:
    """
    Add duration to a datetime string.

    Args:
        base_datetime: "2026-02-05 22:30:00"
        duration: "3 days", "2 hours", "30 minutes", "1 week"

    Returns:
        New datetime string
    """

    # Parsing base datetime
    dt = datetime.strptime(base_datetime, "%Y-%m-%d %H:%M:%S")

    # Parsing duration
    if "day" in duration:
        days = int(duration.split()[0])
        dt = dt + timedelta(days=days)
    elif "week" in duration:
        weeks = int(duration.split()[0])
        dt = dt + timedelta(weeks=weeks)
    elif "hour" in duration:
        hours = int(duration.split()[0])
        dt = dt + timedelta(hours=hours)
    elif "minute" in duration:
        minutes = int(duration.split()[0])
        dt = dt + timedelta(minutes=minutes)

    return dt.strftime("%Y-%m-%d %H:%M:%S")


def set_reminder(reminder_time: str, content: str) -> str:
    """
    Simulate setting a reminder

    Args:
        reminder_time: when to remind
        content; what to remind about

    Returns:
        Confirmation message
    """
    print(f"🔔 Reminder Set: At {reminder_time} - '{content}'")
    return f"🔔 Reminder Set: At {reminder_time} - '{content}'"


function_map = {
    "get_current_time": get_current_time,
    "get_current_date": get_current_date,
    "get_current_datetime": get_current_datetime,
    "add_duration_to_datetime": add_duration_to_datetime,
    "set_reminder": set_reminder,
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
    {
        "type": "function",
        "function": {
            "name": "add_duration_to_datetime",
            "description": "Add a duration to a datetime. Format: YYYY-MM-DD HH:MM:SS",
            "parameters": {
                "type": "object",
                "properties": {
                    "base_datetime": {
                        "type": "string",
                        "description": "Base datetime in YYYY-MM-DD HH:MM:SS format",
                    },
                    "duration": {
                        "type": "string",
                        "description": "Duration to add (e.g., '3 days', '2 hours', '30 minutes', '1 week')",
                    },
                },
                "required": ["base_datetime", "duration"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "set_reminder",
            "description": "Set a reminder for a specific time",
            "parameters": {
                "type": "object",
                "properties": {
                    "reminder_time": {
                        "type": "string",
                        "description": "When to remind (YYYY-MM-DD HH:MM:SS format)",
                    },
                    "content": {
                        "type": "string",
                        "description": "What to remind about",
                    },
                },
                "required": ["reminder_time", "content"],
            },
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

