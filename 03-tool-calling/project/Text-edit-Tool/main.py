import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

API = os.getenv("OPENROUTER_API_KEY")
URL = "https://openrouter.ai/api/v1/"
MODEL = "stepfun/step-3.5-flash:free"


# FUNCTIONS
import os
import json

def read_file(filepath: str) -> str:
    """Read contents of a file"""
    try:
        # Handle relative paths
        if not os.path.isabs(filepath):
            filepath = os.path.join(os.getcwd(), filepath)

        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return f"Error: File '{filepath}' not found"
    except Exception as e:
        return f"Error reading file: {str(e)}"


def write_file(filepath: str, content: str) -> str:
    """Write content to a file (creates or overwrites)"""
    try:
        # Handle relative paths
        if not os.path.isabs(filepath):
            filepath = os.path.join(os.getcwd(), filepath)

        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return f"✅ Successfully wrote to '{filepath}'"
    except Exception as e:
        return f"Error writing file: {str(e)}"


def list_directory(path: str = ".") -> str:
    """List files and directories in a path"""
    try:
        if not os.path.isabs(path):
            path = os.path.join(os.getcwd(), path)

        if not os.path.exists(path):
            return f"Error: Path '{path}' not found"

        items = os.listdir(path)
        result = f"📁 Contents of '{path}':\n"

        for item in items:
            full_path = os.path.join(path, item)
            if os.path.isdir(full_path):
                result += f"📂 {item}/\n"
            else:
                size = os.path.getsize(full_path)
                result += f"📄 {item} ({size} bytes)\n"

        return result
    except Exception as e:
        return f"Error listing directory: {str(e)}"


def edit_file(
    filepath: str,
    old_text: str = None,
    new_text: str = None,
    line_start: int = None,
    line_end: int = None,
) -> str:
    """
    Edit a file: replace text or edit lines
    """
    try:
        if not os.path.isabs(filepath):
            filepath = os.path.join(os.getcwd(), filepath)

        if not os.path.exists(filepath):
            return f"Error: File '{filepath}' not found"

        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()

        if old_text and new_text:
            # Replace text in entire file
            content = "".join(lines)
            if old_text in content:
                new_content = content.replace(old_text, new_text)
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(new_content)
                return f"✅ Replaced '{old_text}' with '{new_text}' in '{filepath}'"
            else:
                return f"❌ Text '{old_text}' not found in file"

        elif line_start is not None and new_text:
            # Edit specific lines (1-indexed)
            if line_start < 1 or line_start > len(lines):
                return f"❌ Line {line_start} out of range (1-{len(lines)})"

            if line_end is None:
                line_end = line_start

            # Replace lines
            lines[line_start - 1 : line_end] = [
                new_text + "\n" if not new_text.endswith("\n") else new_text
            ]

            with open(filepath, "w", encoding="utf-8") as f:
                f.writelines(lines)

            return f"✅ Edited lines {line_start}-{line_end} in '{filepath}'"

        else:
            return "❌ Invalid edit parameters"

    except Exception as e:
        return f"Error editing file: {str(e)}"


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
    "read_file": read_file,
    "write_file": write_file,
    "list_directory": list_directory,
    "edit_file": edit_file,
    "run_batch": run_batch,
}

# FUNCTION_SCHEMAS
tools = []
file_tools = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read contents of a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {"type": "string", "description": "Path to the file"}
                },
                "required": ["filepath"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write content to a file (creates or overwrites)",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {"type": "string", "description": "Path to the file"},
                    "content": {"type": "string", "description": "Content to write"},
                },
                "required": ["filepath", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_directory",
            "description": "List files and directories in a path",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Directory path (default: current directory)",
                    }
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "edit_file",
            "description": "Edit a file: replace text or edit specific lines",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {"type": "string", "description": "Path to the file"},
                    "old_text": {
                        "type": "string",
                        "description": "Text to replace (optional)",
                    },
                    "new_text": {
                        "type": "string",
                        "description": "New text to insert (optional)",
                    },
                    "line_start": {
                        "type": "integer",
                        "description": "Start line number (1-indexed, optional)",
                    },
                    "line_end": {
                        "type": "integer",
                        "description": "End line number (optional)",
                    },
                },
                "required": ["filepath"],
            },
        },
    },
]

tools.extend(file_tools)


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
                                    "read_file",
                                    "write_file",
                                    "list_directory",
                                    "edit_file",
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

# CHAT
messages = [
    {
        "role": "system",
        "content": "You are a helpful assistant that helps in solving day to day problems/queries",
    },
]


def add_assistant_message(text):
    assistance_message = {"role": "assistant", "content": text}
    messages.append(assistance_message)


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
