import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from langchain.messages import HumanMessage
from datetime import timedelta, datetime
import random
import sys
from ddgs import DDGS


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

    if not base_datetime:
        base_datetime = get_current_datetime()

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

def web_search(query: str,max_results:int=5) -> str:
    """Search using DuckDuckGo"""

    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=5))
            return "\n".join([f"{r['title']}:{r['body']}" for r in results])
    except Exception as e:
        return f"{type(e).__name__}: {e}"

function_map = {
    "get_current_time": get_current_time,
    "get_current_date": get_current_date,
    "get_current_datetime": get_current_datetime,
    "add_duration_to_datetime": add_duration_to_datetime,
    "set_reminder": set_reminder,
    "run_batch": run_batch,
    "web_search":web_search
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

tools.append(
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the web for current information",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                },
                "required": ["query"],
            },
        },
    }
)

# Replace your system message
messages = [
    {
        "role": "system",
        "content": """You are a helpful assistant with web search capability.

WHEN YOU RECEIVE SEARCH RESULTS:
1. READ the results carefully
2. SUMMARIZE what you found
3. ANSWER the user's question DIRECTLY
4. NEVER say "let me search more" - you already have the information

Use this to filter relevant results."""
    },
]


def add_assistant_message(text):
    assistant_message = {"role": "assistant", "content": text}
    messages.append(assistant_message)


def add_user_message(text):
    user_message = {"role": "user", "content": text}
    messages.append(user_message)


def chat_stream(message, tools=None, tool_choice=None):
    try:

        client = OpenAI(api_key=API, base_url=URL)

        params = {"model": MODEL, "messages": message, "stream": True}
        if tools:
            params["tools"] = tools
        if tool_choice:
            params["tool_choice"] = tool_choice

        stream = client.chat.completions.create(**params)

        for chunk in stream:
            yield chunk

    except Exception as e:
        print(f"❌ API Error: {type(e).__name__}: {e}")


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


def handle_streaming_tools(user_input):
    """Complete streaming conversation with tool execution"""

    # Add user message to history
    add_user_message(user_input)

    # First API call - get initial response with potential tool calls
    stream = chat_stream(message=messages, tools=tools)

    tool_arguments = {}
    current_tool_name = None
    tool_call_id = None
    response_text = ""

    for chunk in stream:
        if chunk.choices[0].delta and hasattr(chunk.choices[0].delta, "tool_calls"):
            if chunk.choices[0].delta.tool_calls:
                tool_call_delta = chunk.choices[0].delta.tool_calls[0]

                if tool_call_delta.id:
                    tool_call_id = tool_call_delta.id

                if tool_call_delta.function:
                    # Update tool name if present
                    if tool_call_delta.function.name:
                        current_tool_name = tool_call_delta.function.name

                    # Accumulate arguments
                    if tool_call_delta.function.arguments:
                        current_args = tool_arguments.get(current_tool_name, "")
                        tool_arguments[current_tool_name] = (
                            current_args + tool_call_delta.function.arguments
                        )

        # Also handle regular text content
        if chunk.choices[0].delta and chunk.choices[0].delta.content:
            response_text += chunk.choices[0].delta.content
            print(chunk.choices[0].delta.content, end="", flush=True)

    # Store the assistant's response
    if response_text:
        add_assistant_message(response_text)

    # Execute any tools that were called
    if tool_arguments:
        print("\n Executing tools...")

        for tool_name, args in tool_arguments.items():
            try:
                parsed_args = json.loads(args)
                print(f"   {tool_name}: {parsed_args}")

                # Execute the tool
                func = function_map.get(tool_name)
                if func:
                    result = func(**parsed_args)
                    print(f"   Result: {result}")

                    # Send tool result back to AI
                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call_id or "unknown",
                            "content": str(result),
                        }
                    )
                else:
                    print(f"   ❌ Tool {tool_name} not found")

            except json.JSONDecodeError as e:
                print(f"   ❌ Invalid JSON: {args} - Error: {e}")

        # Get final response from AI after tool execution
        print("\n🤖 Final response: ", end="", flush=True)
        final_stream = chat_stream(message=messages, tools=tools)

        final_text = ""
        for chunk in final_stream:
            if chunk.choices[0].delta and chunk.choices[0].delta.content:
                final_text += chunk.choices[0].delta.content
                print(chunk.choices[0].delta.content, end="", flush=True)
                
        if final_text:
            add_assistant_message(final_text)

    print()  # Final newline


def start_chatbot():
    while True:
        user_input = input("You: ")
        if user_input.lower() == "/bye":
            print("Goodbye!")
            break

        print("Bot: ", end="", flush=True)

        try:
            handle_streaming_tools(user_input=user_input)
            print()

        except Exception as e:
            print(f"Error: {type(e).__name__}: {e}")


if __name__ == "__main__":
    start_chatbot()
