import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from langchain.messages import HumanMessage
from datetime import timedelta, datetime
import random
import sys


load_dotenv()

API = os.getenv("OPENROUTER_API_KEY")
MODEL = "meta-llama/llama-3.3-70b-instruct:free"
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
    return f"🔔 Reminder Set: At {reminder_time} - '{content}'"


def run_batch(invocations):
    """Executing multiple tools in paralle"""
    results = []

    for invocation in invocations:
        tool_name = invocation["name"]
        tool_args = invocation["arguments"]
        if isinstance(tool_args, str):
            tool_args = json.loads(tool_args)

        try:
            # calling the actual tool
            tool_func = function_map.get(tool_name)
            if tool_func:
                output = tool_func(**tool_args)
                results.append({"tool": tool_name, "success": True, "output": output})
            else:
                results.append(
                    {
                        "tool": tool_name,
                        "success": False,
                        "error": f"Tool {tool_name} not found",
                    }
                )
        except Exception as e:
            results.append({"tool": tool_name, "success": False, "error": str(e)})
    return results


function_map = {
    "get_current_time": get_current_time,
    "get_current_date": get_current_date,
    "get_current_datetime": get_current_datetime,
    "add_duration_to_datetime": add_duration_to_datetime,
    "set_reminder": set_reminder,
    "run_batch": run_batch,
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

batch_tool_schema = {
    "type": "function",
    "function": {
        "name": "run_batch",
        "description": "Execute multiple tools in parallel. Provide list of tool invocations.",
        "parameters": {
            "type": "object",
            "properties": {
                "invocations": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "Name of tool to run",
                                "enum": [
                                    "get_current_time",
                                    "get_current_date",
                                    "get_current_datetime",
                                    "add_duration_to_datetime",
                                    "set_reminder",
                                ],
                            },
                            "arguments": {
                                "type": "object",
                                "description": "Arguments for the tool",
                            },
                        },
                        "required": ["name", "arguments"],
                    },
                }
            },
            "required": ["invocations"],
        },
    },
}

tools.append(batch_tool_schema)


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
        return completion

    except ValueError as e:
        print(e)


print("👋 Welcome! I'm your chatbot. Type '/bye' to end the chat.\n")


def execute_tool_calls(tool_calls):
    results = []

    for tool_call in tool_calls:
        args = (
            json.loads(tool_call.function.arguments)
            if tool_call.function.arguments
            else {}
        )
        func_name = tool_call.function.name
        print(f"Tool name: {func_name}")

        if func_name == "run_batch":
            # Run batch and format EACH tool's result separately
            batch_results = run_batch(**args)

            # Format each tool's result
            formatted_batch = []
            for batch_item in batch_results:
                tool_name = batch_item["tool"]
                status = "✅" if batch_item["success"] else "❌"
                output = batch_item.get("output", batch_item.get("error", "No output"))
                formatted_batch.append(f"{status} {tool_name}: {output}")

            results.append(
                {
                    "tool_call_id": tool_call.id,
                    "content": "\n".join(formatted_batch),  # Send readable text
                }
            )
        else:
            # Normal single tool execution
            func = function_map.get(func_name)
            if func:
                try:
                    result = func(**args)
                    results.append(
                        {"tool_call_id": tool_call.id, "content": str(result)}
                    )
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

    # clear any pending prints
    sys.stdout.flush()

    # adding loop to handle multiple tool call rounds
    max_iterations = 5
    current_iteration = 0

    while current_iteration < max_iterations:
        current_iteration += 1

        # 1st API call
        completion = chat(message=messages, tools=tools)

        if (
            not completion
            or not hasattr(completion, "choices")
            or not completion.choices
        ):
            print("DEBUG: No valid response from API")
            return None

        message_obj = completion.choices[0].message

        # Adding AI's response to conversation history
        messages.append(message_obj)

        # checking wheather the response is calling a tool
        if hasattr(message_obj, "tool_calls") and message_obj.tool_calls:
            print(f"DEBUG: AI wanna use {len(message_obj.tool_calls)} tool(s)")

            # Executing tools
            tool_results = execute_tool_calls(tool_calls=message_obj.tool_calls)

            ## Sending the function result back to the AI model
            for result in tool_results:
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": result["tool_call_id"],
                        "content": result["content"],
                    }
                )

            continue

        else:
            if message_obj.content:
                add_assistant_message(message_obj.content)
                return message_obj.content
            else:
                print("Bot: (No response content)\n")
    return "Reached maximum iterations"


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
