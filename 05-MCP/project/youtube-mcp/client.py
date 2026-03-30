import asyncio
import json
import os
from mcp import ClientSession, StdioServerParameters, stdio_client
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

API = os.getenv("OPENROUTER_API_KEY")
MODEL = "nvidia/nemotron-3-nano-30b-a3b:free"
URL = "https://openrouter.ai/api/v1/"


class MCPClient:
    def __init__(self):
        self.session = None
        self.tools = None
        self._stdio = None
        self._session_ctx = None

    async def connect(self):
        server_params = StdioServerParameters(
            command="uvx",
            args=[
                "--from",
                "git+https://github.com/jkawamoto/mcp-youtube-transcript",
                "mcp-youtube-transcript",
                "--response-limit",
                "15000",
            ],
        )

        self._stdio = stdio_client(server_params)
        read, write = await self._stdio.__aenter__()

        self._session_ctx = ClientSession(read, write)
        self.session = await self._session_ctx.__aenter__()

        await self.session.initialize()
        tool_result = await self.session.list_tools()
        self.tools = [t.model_dump() for t in tool_result.tools]
        print(f"✅ connected with {len(self.tools)} tools")
        return self.session, self.tools

    async def close(self):
        if self._session_ctx:
            await self._session_ctx.__aexit__(None, None, None)
        if self._stdio:
            await self._stdio.__aexit__(None, None, None)
        self.session = None
        self.tools = None
        print("🔌 Disconnected")


mcp = MCPClient()

messages = [
    {
        "role": "system",
        "content": "You are a helpful assistant with access to YouTube transcript tool.",
    }
]


def add_assistant_message(text):
    messages.append({"role": "assistant", "content": text})


def add_user_message(text):
    messages.append({"role": "user", "content": text})


def chat_stream(message, tools=None, max_tokens=8000):
    try:
        client = OpenAI(api_key=API, base_url=URL)
        params = {
            "model": MODEL,
            "messages": message,
            "stream": True,
            "max_tokens": max_tokens,
        }
        if tools:
            params["tools"] = tools

        stream = client.chat.completions.create(**params)
        for chunk in stream:
            yield chunk

    except Exception as e:
        print(f"❌ API Error: {type(e).__name__}: {e}")


async def handle_streaming_tools(user_input, session, tools):
    tool_calls_accumulator = {}
    response_text = ""

    mcp_tools = []
    for tool in tools:
        mcp_tools.append({
            "type": "function",
            "function": {
                "name": tool["name"],
                "description": tool["description"],
                "parameters": tool["inputSchema"],
            },
        })

    add_user_message(user_input)

    stream = chat_stream(message=messages, tools=mcp_tools)

    for chunk in stream:
        if chunk.choices[0].delta.tool_calls:
            for i, tool_call_delta in enumerate(chunk.choices[0].delta.tool_calls):
                if i not in tool_calls_accumulator:
                    tool_calls_accumulator[i] = {"id": None, "name": None, "arguments": ""}

                if tool_call_delta.id:
                    tool_calls_accumulator[i]["id"] = tool_call_delta.id
                if tool_call_delta.function and tool_call_delta.function.name:
                    tool_calls_accumulator[i]["name"] = tool_call_delta.function.name
                if tool_call_delta.function and tool_call_delta.function.arguments:
                    tool_calls_accumulator[i]["arguments"] += tool_call_delta.function.arguments

        if chunk.choices[0].delta and chunk.choices[0].delta.content:
            response_text += chunk.choices[0].delta.content
            print(chunk.choices[0].delta.content, end="", flush=True)

    if response_text:
        add_assistant_message(response_text)

    if tool_calls_accumulator:
        print("\n🔧 Executing tools...")

        for idx, tool_data in tool_calls_accumulator.items():
            if not tool_data["name"]:
                continue

            try:
                parsed_args = json.loads(tool_data["arguments"])
                print(f"   {tool_data['name']}: {parsed_args}")

                result = await session.call_tool(name=tool_data["name"], arguments=parsed_args)

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_data["id"] or f"call_{idx}",
                    "content": str(result),
                })

            except json.JSONDecodeError as e:
                print(f"   ❌ Invalid JSON: {e}")

        print("\n🤖 ", end="", flush=True)
        final_stream = chat_stream(message=messages, tools=mcp_tools)

        final_text = ""
        for chunk in final_stream:
            if chunk.choices[0].delta and chunk.choices[0].delta.content:
                final_text += chunk.choices[0].delta.content
                print(chunk.choices[0].delta.content, end="", flush=True)

        if final_text:
            add_assistant_message(final_text)

    print()


async def start_chatbot():
    await mcp.connect()
    print("👋 Welcome! I'm your chatbot. Type '/bye' to end the chat.\n")

    try:
        while True:
            user_input = input("You: ")
            if user_input.lower() == "/bye":
                print("Goodbye!")
                break

            print("Bot: ", end="", flush=True)

            try:
                await handle_streaming_tools(user_input, mcp.session, mcp.tools)
                print()
            except Exception as e:
                print(f"Error: {type(e).__name__}: {e}")
    finally:
        await mcp.close()


async def main():
    await start_chatbot()


if __name__ == "__main__":
    asyncio.run(main())