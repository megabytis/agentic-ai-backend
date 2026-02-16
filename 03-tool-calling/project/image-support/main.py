import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from datetime import timedelta, datetime
import sys
from ddgs import DDGS
import base64
from pathlib import Path

load_dotenv()

API = os.getenv("OPENROUTER_API_KEY")
MODEL = "qwen/qwen3-vl-235b-a22b-thinking"
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


def web_search(query: str, max_results: int = 10, allowed_domains: list = None) -> str:
    """Search using DuckDuckGo & optionally restrict to specific domains"""

    # appending current year if not present
    current_year = datetime.now().year
    if str(current_year) not in query:
        query = f"{query} {current_year}"

    # Now adding domain restrictions to query if specified
    original_query = query
    if allowed_domains:
        domain_query = " OR ".join([f"site: {domain}" for domain in allowed_domains])

        query = f"({original_query}) {domain_query}"

    print(f"\n🔍 WEB SEARCH: '{query}'")

    if allowed_domains:
        print(f"Restricted to domains: {', '.join(allowed_domains)}")
        print(f"Max results: {max_results}")

    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))

            if not results:
                return "No search results found"

            formatted = []
            for i, r in enumerate(results, 1):
                title = r.get("title", "No title")
                body = r.get("body", "No content")
                url = r.get("href", "No URL")

                if allowed_domains:
                    if not any(domain in url for domain in allowed_domains):
                        continue

                formatted.append(f"{i}. {title}")
                formatted.append(f"  {body}")
                formatted.append(f"  Source: {url}\n")

            if not formatted:
                return f"No results found from domains: {allowed_domains}"

            print(f"    Found {len(formatted)//3} results")
            return "\n".join(formatted)

    except ImportError:
        return "ERROR: ddgs page package is not installed. Run: pip install ddgs"
    except Exception as e:
        return f"Search failed: {str(e)}"


def encode_image(images_path):
    """Converting image to base64 string"""
    with open(images_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def create_image_message(image_path, prompt_text):
    """Creating a message with image and text"""

    # Encoding image
    image_base64 = encode_image(image_path)

    # Determining image type
    ext = Path(image_path).suffix.lower()
    media_type = {
        ".png": "image/png",
        ".jpg": "image/jpeg",  # Fixed: .jpg should be image/jpeg, not image/jpg
        ".jpeg": "image/jpeg",
        ".gif": "image/gif",
        ".webp": "image/webp",
    }.get(ext, "image/png")

    # FIXED: Remove space after comma and lowercase 'data'
    message = {
        "role": "user",
        "content": [
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:{media_type};base64,{image_base64}"
                },  # <-- FIX HERE
            },
            {"type": "text", "text": prompt_text},
        ],
    }

    return message


def analyze_image(image_path, prompt_text):
    """Sending image to AI for analysis"""

    # Creating message with image
    image_message = create_image_message(image_path=image_path, prompt_text=prompt_text)

    # Using temporary message
    temp_messages = [image_message]

    print(f"\n🖼️ Analyzing image: {image_path}")
    print(f"📝 Prompt: {prompt_text[:50]}...\n")

    print("🤖 Response: ", end="", flush=True)

    response_text = ""
    stream = chat_stream(message=temp_messages, max_tokens=4000)

    for chunk in stream:
        if chunk.choices[0].delta and chunk.choices[0].delta.content:
            content = chunk.choices[0].delta.content
            response_text += content
            print(content, end="", flush=True)

    print("\n")
    return response_text


def handle_image_command(image_path, custom_prompt=None):
    """Handle image upload/analysis in chat"""

    default_prompt = "Describe this image in detail. What do you see?"
    prompt = custom_prompt or default_prompt

    return analyze_image(image_path, prompt)


function_map = {
    "get_current_time": get_current_time,
    "get_current_date": get_current_date,
    "get_current_datetime": get_current_datetime,
    "add_duration_to_datetime": add_duration_to_datetime,
    "set_reminder": set_reminder,
    "run_batch": run_batch,
    "web_search": web_search,
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
            "description": "Search the web for current information, optionally restrict to specific domains",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of results to return (default: 10)",
                    },
                    "allowed_domains": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Restrict search to these domains (e.g., ['nih.gov', 'reuters.com'])",
                    },
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

Use this to filter relevant results.""",
    },
]


def add_assistant_message(text):
    assistant_message = {"role": "assistant", "content": text}
    messages.append(assistant_message)


def add_user_message(text):
    user_message = {"role": "user", "content": text}
    messages.append(user_message)


def chat_stream(
    message,
    tools=None,
    tool_choice=None,
    thinking=False,
    thinking_budget=2048,
    max_tokens=8000,
):
    """Streaming version with thinking support"""
    try:

        client = OpenAI(api_key=API, base_url=URL)

        params = {
            "model": MODEL,
            "messages": message,
            "stream": True,
            "max_tokens": max_tokens,  # Must be > thinking_budget
        }

        if tools:
            params["tools"] = tools
        if tool_choice:
            params["tool_choice"] = tool_choice

        # Adding thinking
        if thinking:
            params["thinking"] = {"type": "enabled", "budget_tokens": thinking_budget}

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


def handle_streaming_tools(user_input, thinking=False):
    """Complete streaming conversation with tool execution"""

    if thinking:
        enhanced_input = f"""Let's think through this step by step: 
        
        Question: {user_input}
        
        First, I'll break this down:
        """
    else:
        enhanced_input = user_input

    # Add user message to history
    add_user_message(user_input)

    # First API call - get initial response with potential tool calls
    stream = chat_stream(
        message=messages,
        tools=tools,
        thinking=thinking,
        thinking_budget=2048,
        max_tokens=8000,
    )

    tool_arguments = {}
    current_tool_name = None
    tool_call_id = None
    response_text = ""

    for chunk in stream:
        # Checking for thinking content
        if (
            hasattr(chunk.choices[0].delta, "thinking")
            and chunk.choices[0].delta.thinking
        ):
            thinking_text = chunk.choices[0].delta.thinking
            print(f"\n💭 {thinking_text}", end="", flush=True)

        # Checking for reasoning (alternative name of thinking)
        elif (
            hasattr(chunk.choices[0].delta, "reasoning")
            and chunk.choices[0].delta.reasoning
        ):
            reasoning_text = chunk.choices[0].delta.reasoning
            print(f"\n💭 {reasoning_text}", end="", flush=True)

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
    thinking_enabled = False

    while True:
        user_input = input("You: ")
        if user_input.lower() == "/bye":
            print("Goodbye!")
            break
        elif user_input.lower() == "/think":
            thinking_enabled = not thinking_enabled
            print(f"Thinking mode: {'ON' if thinking_enabled else 'OFF'}")
            continue
        elif user_input.lower().startswith("/image "):
            # Format: /image path/to/image.jpg [optional]
            parts = user_input.split(" ", 2)
            image_path = parts[1]
            custom_prompt = parts[2] if len(parts) > 2 else None

            try:
                handle_image_command(image_path=image_path, custom_prompt=custom_prompt)
            except Exception as e:
                print(f"❌ Error analyzing image: {e}")
            continue

        print("Bot: ", end="", flush=True)

        try:
            handle_streaming_tools(user_input=user_input, thinking=thinking_enabled)
            print()

        except Exception as e:
            print(f"Error: {type(e).__name__}: {e}")


if __name__ == "__main__":
    start_chatbot()
