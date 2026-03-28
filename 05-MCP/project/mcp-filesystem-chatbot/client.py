"""
Simple MCP Client that connects to a local MCP server
"""

import json
import subprocess
import sys
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class MCPClient:
    def __init__(self, server_command):
        """
        server_command: list of commands to start the MCP server
        Example: ["npx", "-y", "@modelcontextprotocol/server-filesystem", "/path/to/workspace"]
        """
        self.server_process = subprocess.Popen(
            server_command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        self.request_id = 0
        self.tools = []
        self._handshake()
    
    def _handshake(self):
        """Initial connection to server"""
        # Send initialization request
        self._send_request("initialize", {
            "protocolVersion": "0.1.0",
            "capabilities": {}
        })
        # Receive response
        self._read_response()
    
    def _send_request(self, method, params=None):
        self.request_id += 1
        request = {
            "jsonrpc": "2.0",
            "method": method,
            "id": self.request_id
        }
        if params:
            request["params"] = params
        
        self.server_process.stdin.write(json.dumps(request) + "\n")
        self.server_process.stdin.flush()
    
    def _read_response(self):
        """Read one response from server"""
        line = self.server_process.stdout.readline()
        if line:
            return json.loads(line)
        return None
    
    def list_tools(self):
        """Get all available tools from MCP server"""
        self._send_request("tools/list")
        response = self._read_response()
        if response and "result" in response:
            self.tools = response["result"]["tools"]
            return self.tools
        return []
    
    def call_tool(self, tool_name, arguments):
        """Execute a tool on the MCP server"""
        self._send_request("tools/call", {
            "name": tool_name,
            "arguments": arguments
        })
        response = self._read_response()
        if response and "result" in response:
            return response["result"]["content"]
        return {"error": "Tool call failed"}
    
    def close(self):
        """Clean up server process"""
        self.server_process.terminate()


def convert_mcp_tools_to_openai_format(mcp_tools):
    """
    Convert MCP tool format to OpenAI function format
    """
    openai_tools = []
    for tool in mcp_tools:
        openai_tools.append({
            "type": "function",
            "function": {
                "name": tool["name"],
                "description": tool.get("description", ""),
                "parameters": tool.get("inputSchema", {"type": "object", "properties": {}})
            }
        })
    return openai_tools


def main():
    print("=" * 50)
    print("🤖 MCP-Powered Chatbot")
    print("=" * 50)
    
    # Step 1: Start the MCP server
    # This server gives us filesystem tools
    workspace = os.getcwd()  # Current directory for file operations
    
    print(f"\n📁 Starting filesystem MCP server...")
    print(f"   Workspace: {workspace}")
    
    mcp = MCPClient([
        "npx", "-y", "@modelcontextprotocol/server-filesystem", workspace
    ])
    
    # Step 2: Get all tools from the MCP server
    print("\n🔧 Fetching tools from MCP server...")
    mcp_tools = mcp.list_tools()
    
    print(f"   Found {len(mcp_tools)} tool(s):")
    for tool in mcp_tools:
        print(f"   - {tool['name']}: {tool.get('description', 'No description')}")
    
    # Step 3: Convert to OpenAI format
    openai_tools = convert_mcp_tools_to_openai_format(mcp_tools)
    
    # Step 4: Initialize OpenRouter client
    print("\n🤖 Initializing LLM...")
    llm = OpenAI(
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1"
    )
    model = "stepfun/step-3.5-flash:free"  # Free model
    
    # Step 5: Start chat loop
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant with filesystem access. You can read, write, and list files. Use these tools when needed."
        }
    ]
    
    print("\n" + "=" * 50)
    print("Chat started! Type 'quit' to exit")
    print("Try: 'list files in current directory'")
    print("     'create a file called hello.txt with Hello World'")
    print("     'read hello.txt'")
    print("=" * 50 + "\n")
    
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "quit":
            break
        
        messages.append({"role": "user", "content": user_input})
        
        # Get response from LLM (may include tool calls)
        response = llm.chat.completions.create(
            model=model,
            messages=messages,
            tools=openai_tools,
            tool_choice="auto"
        )
        
        message = response.choices[0].message
        messages.append(message)
        
        # Handle tool calls
        if message.tool_calls:
            print("\n🔧 Executing tool(s)...")
            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)
                
                print(f"   Tool: {tool_name}")
                print(f"   Args: {args}")
                
                # Call the tool via MCP server
                result = mcp.call_tool(tool_name, args)
                
                print(f"   Result: {str(result)[:200]}...")
                
                # Add tool result to messages
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result)
                })
            
            # Get final response after tool execution
            final = llm.chat.completions.create(
                model=model,
                messages=messages
            )
            final_message = final.choices[0].message
            messages.append(final_message)
            print(f"\n🤖 Bot: {final_message.content}")
        else:
            print(f"\n🤖 Bot: {message.content}")
    
    mcp.close()
    print("\nGoodbye!")


if __name__ == "__main__":
    main()